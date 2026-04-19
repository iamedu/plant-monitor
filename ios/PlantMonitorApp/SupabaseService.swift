import Foundation

final class SupabaseService {
    private let config: SupabaseConfig
    private let session: URLSession

    init(session: URLSession = .shared) throws {
        self.session = session
        self.config = try Self.loadConfig()
    }

    func fetchReadings(limit: Int = 50) async throws -> [PlantReading] {
        guard var components = URLComponents(string: config.url + "/rest/v1/" + config.table) else {
            throw URLError(.badURL)
        }
        components.queryItems = [
            URLQueryItem(name: "select", value: "id,ts,temperature_c,humidity_percent,soil_moisture_percent,light_lux,needs_water"),
            URLQueryItem(name: "order", value: "ts.desc"),
            URLQueryItem(name: "limit", value: String(limit))
        ]
        guard let url = components.url else { throw URLError(.badURL) }

        var request = URLRequest(url: url)
        request.setValue(config.publishableKey, forHTTPHeaderField: "apikey")
        request.setValue("Bearer \(config.publishableKey)", forHTTPHeaderField: "Authorization")

        let (data, response) = try await session.data(for: request)
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw URLError(.badServerResponse)
        }
        return try JSONDecoder().decode([PlantReading].self, from: data)
    }

    private static func loadConfig() throws -> SupabaseConfig {
        guard let url = Bundle.main.url(forResource: "SupabaseConfig", withExtension: "json") else {
            throw NSError(domain: "PlantMonitorApp", code: 1, userInfo: [NSLocalizedDescriptionKey: "Missing SupabaseConfig.json"])
        }
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode(SupabaseConfig.self, from: data)
    }
}
