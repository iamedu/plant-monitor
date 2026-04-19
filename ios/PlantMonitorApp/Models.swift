import Foundation

struct SupabaseConfig: Decodable {
    let url: String
    let publishableKey: String
    let table: String

    enum CodingKeys: String, CodingKey {
        case url
        case publishableKey = "publishable_key"
        case table
    }
}

struct PlantReading: Identifiable, Decodable {
    var id: Int?
    let ts: String
    let temperatureC: Double?
    let humidityPercent: Double?
    let soilMoisturePercent: Double?
    let lightLux: Double?
    let needsWater: Bool?

    enum CodingKeys: String, CodingKey {
        case id
        case ts
        case temperatureC = "temperature_c"
        case humidityPercent = "humidity_percent"
        case soilMoisturePercent = "soil_moisture_percent"
        case lightLux = "light_lux"
        case needsWater = "needs_water"
    }

    var timestamp: Date? {
        ISO8601DateFormatter().date(from: ts)
    }

    var moistureText: String {
        guard let soilMoisturePercent else { return "—" }
        return String(format: "%.1f%%", soilMoisturePercent)
    }

    var tempText: String {
        guard let temperatureC else { return "—" }
        return String(format: "%.0f°C", temperatureC)
    }

    var humidityText: String {
        guard let humidityPercent else { return "—" }
        return String(format: "%.0f%%", humidityPercent)
    }

    var lightText: String {
        guard let lightLux else { return "—" }
        return String(format: "%.0f lx", lightLux)
    }
}
