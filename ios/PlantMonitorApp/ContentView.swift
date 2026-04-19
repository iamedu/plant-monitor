import SwiftUI

struct ContentView: View {
    @EnvironmentObject var store: ReadingsStore

    var body: some View {
        NavigationStack {
            List {
                if let latest = store.latest {
                    Section("Latest") {
                        LatestReadingCard(reading: latest)
                            .listRowInsets(EdgeInsets())
                            .padding(.vertical, 8)
                    }
                }

                Section("Recent History") {
                    ForEach(store.readings) { reading in
                        ReadingRow(reading: reading)
                    }
                }
            }
            .overlay {
                if store.readings.isEmpty && !store.isLoading {
                    ContentUnavailableView("No readings yet", systemImage: "leaf")
                }
            }
            .navigationTitle("Plant Monitor")
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    if store.isLoading {
                        ProgressView()
                    }
                }
            }
            .refreshable {
                await store.refresh()
            }
            .alert("Error", isPresented: .constant(store.errorMessage != nil), actions: {
                Button("OK") { store.errorMessage = nil }
            }, message: {
                Text(store.errorMessage ?? "Unknown error")
            })
        }
    }
}

struct LatestReadingCard: View {
    let reading: PlantReading

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Label(reading.needsWater == true ? "Needs water" : "Looking good", systemImage: reading.needsWater == true ? "drop.triangle" : "checkmark.circle.fill")
                    .font(.headline)
                    .foregroundStyle(reading.needsWater == true ? .orange : .green)
                Spacer()
                if let date = reading.timestamp {
                    Text(date, style: .relative)
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }

            HStack(spacing: 12) {
                MetricView(title: "Soil", value: reading.moistureText)
                MetricView(title: "Temp", value: reading.tempText)
                MetricView(title: "Humidity", value: reading.humidityText)
                MetricView(title: "Light", value: reading.lightText)
            }
        }
        .padding()
        .background(.thinMaterial, in: RoundedRectangle(cornerRadius: 16))
    }
}

struct MetricView: View {
    let title: String
    let value: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title)
                .font(.caption)
                .foregroundStyle(.secondary)
            Text(value)
                .font(.headline)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

struct ReadingRow: View {
    let reading: PlantReading

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(reading.timestamp ?? Date(), style: .time)
                    .font(.headline)
                Spacer()
                Text(reading.needsWater == true ? "Water" : "OK")
                    .font(.caption.weight(.semibold))
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background((reading.needsWater == true ? Color.orange : Color.green).opacity(0.15), in: Capsule())
            }
            Text("Soil \(reading.moistureText) • Temp \(reading.tempText) • Humidity \(reading.humidityText) • Light \(reading.lightText)")
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }
}
