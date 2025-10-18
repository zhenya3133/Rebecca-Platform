export type TestConnectionResponse = {
  ok: boolean;
};

const DEFAULT_ENDPOINT = "http://localhost:8000";

export class RebeccaCoreService {
  static async testConnection(endpoint: string, token: string): Promise<boolean> {
    const target = endpoint || DEFAULT_ENDPOINT;
    try {
      const response = await fetch(`${target}/health`, {
        method: "GET",
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      });
      return response.ok;
    } catch (error) {
      console.warn("Rebecca core connection failed", error);
      return false;
    }
  }
}