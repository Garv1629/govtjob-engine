import { fetchApi } from "../lib/api";

describe("Frontend API Client Integration Tests", () => {
  beforeEach(() => {
    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test("fetchApi successfully parses JSON response", async () => {
    const mockData = { status: "HEALTHY", timestamp: "2026-08-04T12:00:00Z" };
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockData,
    });

    const result = await fetchApi<{ status: string }>("/health");
    expect(result.status).toBe("HEALTHY");
    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/health"),
      expect.objectContaining({
        headers: expect.objectContaining({
          "Content-Type": "application/json",
        }),
      })
    );
  });

  test("fetchApi throws structured error on HTTP failure", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      statusText: "Internal Server Error",
    });

    await expect(fetchApi("/error-endpoint")).rejects.toThrow("API Error 500: Internal Server Error");
  });
});
