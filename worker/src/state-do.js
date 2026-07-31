import { DurableObject } from "cloudflare:workers";

// Single global instance — strongly consistent reads/writes, no KV propagation lag.
export class ProfileState extends DurableObject {
  async get(key) {
    return (await this.ctx.storage.get(key)) ?? null;
  }

  async put(key, value) {
    await this.ctx.storage.put(key, value);
  }
}
