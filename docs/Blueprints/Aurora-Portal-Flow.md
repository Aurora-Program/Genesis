# Aurora Portal — Flujo extremo a extremo

1) Navegador → Autenticación descentralizada (DID/Wallet) → Perfil on-chain
2) Aparición del Agente-Operador (chat) → intención del usuario
3) Ofertas/Bids → selección de N réplicas → Contrato de Sesión on-chain (escrow + SLO)
4) Plano P2P (WebRTC/libp2p): ejecución cifrada, replicación/erasure coding, verificación
5) Attestations/Oráculos → liquidación on-chain → tokens y reputación actualizados

APIs mínimas (lado agente):
- market.discover(filter) -> services[]
- market.request(service_id, offer) -> bids[]
- market.select(bids, policy) -> selection
- session.open(selection, stake) -> session_id
- session.metrics(session_id) -> live_stats
- session.close(session_id) -> settlement
- dispute.open(session_id, evidence[]) -> case_id
