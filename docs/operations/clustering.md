# Optional clustering

Plainwire has an optional cluster profile. It is not required for normal self-hosting.

## Before adding app nodes

Make sure you already have:

- external or shared PostgreSQL;
- Redis with a stable unique `PLAINWIRE_NODE_ID` per node;
- shared/durable upload strategy;
- reverse-proxy routing plan;
- metrics that identify per-node failures;
- tested session/WebSocket reconnect behavior.

## Build

The upstream project uses a separate `cluster` rebar profile with Partisan. Default builds do not download or start it.

## WebSocket ownership

Do not blindly distribute a single WebSocket across nodes without respecting Plainwire's ownership model. Sticky routing or explicit connection ownership may be needed depending on the cluster transport design.

## Why not start clustered

One reliable app host plus an external database is easier to operate than three app hosts with poorly understood shared state. Scale application nodes when CPU, connections, availability targets, or maintenance requirements justify them.
