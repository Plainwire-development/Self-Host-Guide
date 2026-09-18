# Glossary

**BEAM**  
The Erlang virtual machine that runs Plainwire.

**Cowboy**  
The Erlang HTTP/WebSocket server used by Plainwire.

**ICE**  
The WebRTC process that gathers and tests network paths.

**STUN**  
Helps a client discover its public-facing network mapping. It does not relay media.

**TURN**  
Relays WebRTC media when direct connectivity fails.

**Coturn**  
A widely used open-source STUN/TURN server.

**Redis**  
In-memory data store used by Plainwire for ephemeral distributed acceleration.

**ScyllaDB**  
Distributed wide-column database used by Plainwire as an optional high-volume history backend.

**CQL**  
Cassandra Query Language, used by ScyllaDB.

**Outbox**  
A durable PostgreSQL queue that records work that must be delivered to another system such as Scylla.

**Recovery mirror**  
PostgreSQL message data retained while Scylla is becoming authoritative so rollback and repair remain possible.

**Reverse proxy**  
Public HTTP server such as Caddy or nginx that handles TLS and forwards requests to Plainwire.

**RPO**  
Recovery Point Objective, the amount of data loss a recovery plan allows.

**RTO**  
Recovery Time Objective, how long service restoration may take.
