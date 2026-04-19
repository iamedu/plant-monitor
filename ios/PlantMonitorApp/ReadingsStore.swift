import Foundation

@MainActor
final class ReadingsStore: ObservableObject {
    @Published var readings: [PlantReading] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let service: SupabaseService?

    init() {
        self.service = try? SupabaseService()
        if service == nil {
            self.errorMessage = "Missing or invalid Supabase config"
        }
    }

    var latest: PlantReading? { readings.first }

    func refresh() async {
        guard let service else { return }
        isLoading = true
        defer { isLoading = false }
        do {
            readings = try await service.fetchReadings(limit: 50)
            errorMessage = nil
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
