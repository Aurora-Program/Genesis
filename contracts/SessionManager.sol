// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title SessionManager - Esqueleto de contratos de sesión para Aurora Portal
/// @notice Interface mínima para registrar servicios, publicar ofertas, recibir bids,
///         abrir sesiones replicadas, reportar attestations y liquidar pagos con bonos/slashing.
contract SessionManager {
    enum SessionState { None, Offered, Open, Closed, Disputed, Settled }

    struct Service {
        bytes32 id;           // hash determinista del descriptor (ej. keccak256(CID))
        address owner;        // dueño del servicio (cobra royalties si aplica)
        string cid;           // descriptor CID/IPFS del servicio/modelo
        uint16 minReplicas;   // mínimo de réplicas requerido
        address mgmtModel;    // referencia a modelo de gestión (política de precios/SLO)
    }

    struct Offer {
        bytes32 id;           // id de la oferta
        bytes32 serviceId;    // referencia al servicio
        address client;       // agente que solicita la sesión
        uint64 start;         // ventana de inicio (epoch)
        uint64 duration;      // duración en segundos
        uint256 clientStake;  // stake en escrow del cliente
        bytes32 SLOhash;      // hash de los SLOs pactados
    }

    struct Bid {
        address node;         // nodo proveedor
        uint256 price;        // precio propuesto (total o por unidad de tiempo)
        uint256 capacity;     // capacidad comprometida (unidades dependientes del tipo)
        string evidenceCID;   // evidencias/reputación/metrics (CID)
    }

    struct Session {
        bytes32 id;           // id de la sesión
        bytes32 offerId;      // referencia a la oferta
        bytes32 serviceId;    // referencia al servicio
        address client;       // cliente
        address[] nodes;      // nodos seleccionados (réplicas)
        uint256 escrow;       // escrow total bloqueado
        uint64 start;         // inicio acordado
        uint64 end;           // fin (actual o esperado)
        SessionState state;   // estado
    }

    // storage
    mapping(bytes32 => Service) public services;
    mapping(bytes32 => Offer) public offers;
    mapping(bytes32 => Session) public sessions;
    mapping(bytes32 => Bid[]) public offerBids;

    // events
    event ServiceRegistered(bytes32 indexed serviceId, address indexed owner, string cid, uint16 minReplicas, address mgmtModel);
    event OfferPosted(bytes32 indexed offerId, bytes32 indexed serviceId, address indexed client);
    event BidPlaced(bytes32 indexed offerId, address indexed node, uint256 price, uint256 capacity);
    event SessionOpened(bytes32 indexed sessionId, bytes32 indexed offerId, address indexed client, address[] nodes, uint256 escrow);
    event Attestation(bytes32 indexed sessionId, address indexed reporter, string metricCID);
    event Settled(bytes32 indexed sessionId, uint256[] payouts, uint256 slashed);

    // --- API ---

    function registerService(string calldata cid, uint16 minReplicas, address mgmtModel) external returns (bytes32 serviceId) {
        serviceId = keccak256(abi.encodePacked(msg.sender, cid, minReplicas, mgmtModel));
        require(services[serviceId].owner == address(0), "SERVICE_EXISTS");
        services[serviceId] = Service({
            id: serviceId,
            owner: msg.sender,
            cid: cid,
            minReplicas: minReplicas,
            mgmtModel: mgmtModel
        });
        emit ServiceRegistered(serviceId, msg.sender, cid, minReplicas, mgmtModel);
    }

    function postOffer(bytes32 serviceId, uint64 start, uint64 duration, bytes32 SLOhash) external payable returns (bytes32 offerId) {
        require(services[serviceId].owner != address(0), "SERVICE_UNKNOWN");
        require(msg.value > 0, "STAKE_REQUIRED");
        offerId = keccak256(abi.encodePacked(msg.sender, serviceId, start, duration, SLOhash, block.timestamp));
        offers[offerId] = Offer({
            id: offerId,
            serviceId: serviceId,
            client: msg.sender,
            start: start,
            duration: duration,
            clientStake: msg.value,
            SLOhash: SLOhash
        });
        emit OfferPosted(offerId, serviceId, msg.sender);
    }

    function placeBid(bytes32 offerId, uint256 price, uint256 capacity, string calldata evidenceCID) external returns (bool) {
        Offer memory off = offers[offerId];
        require(off.client != address(0), "OFFER_UNKNOWN");
        offerBids[offerId].push(Bid({ node: msg.sender, price: price, capacity: capacity, evidenceCID: evidenceCID }));
        emit BidPlaced(offerId, msg.sender, price, capacity);
        return true;
    }

    function openSession(bytes32 offerId, address[] calldata selectedNodes) external returns (bytes32 sessionId) {
        Offer memory off = offers[offerId];
        require(off.client == msg.sender, "ONLY_CLIENT");
        require(selectedNodes.length >= services[off.serviceId].minReplicas, "REPLICAS_LT_MIN");
        sessionId = keccak256(abi.encodePacked(offerId, selectedNodes, block.timestamp));
        sessions[sessionId] = Session({
            id: sessionId,
            offerId: offerId,
            serviceId: off.serviceId,
            client: off.client,
            nodes: selectedNodes,
            escrow: off.clientStake,
            start: off.start,
            end: off.start + off.duration,
            state: SessionState.Open
        });
        emit SessionOpened(sessionId, offerId, off.client, selectedNodes, off.clientStake);
    }

    function submitAttestation(bytes32 sessionId, string calldata metricCID) external {
        Session storage s = sessions[sessionId];
        require(s.client != address(0), "SESSION_UNKNOWN");
        // Nota: en MVP no validamos lista de reporteros; se hará vía mgmtModel/oracles
        emit Attestation(sessionId, msg.sender, metricCID);
    }

    function settleSession(bytes32 sessionId) external {
        Session storage s = sessions[sessionId];
        require(s.client != address(0), "SESSION_UNKNOWN");
        require(s.state == SessionState.Open || s.state == SessionState.Closed, "BAD_STATE");
        // MVP: distribuir escrow a nodos a partes iguales (reemplazar por lógica mgmtModel + attestations)
        uint256 n = s.nodes.length;
        uint256 perNode = s.escrow / (n == 0 ? 1 : n);
        uint256[] memory payouts = new uint256[](n);
        uint256 slashed = 0;
        for (uint256 i = 0; i < n; i++) {
            payouts[i] = perNode;
            (bool ok, ) = s.nodes[i].call{value: perNode}("");
            require(ok, "TRANSFER_FAIL");
        }
        s.state = SessionState.Settled;
        emit Settled(sessionId, payouts, slashed);
    }

    // fallback para recibir stakes
    receive() external payable {}
}
