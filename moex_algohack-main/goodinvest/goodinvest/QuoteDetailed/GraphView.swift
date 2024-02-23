import SwiftUI
import Charts
import Combine
import Foundation

class GraphViewModel: ObservableObject {
		@Published var graphData: [GraphModel] = []
}

struct GraphView: View {
		@ObservedObject var viewModel: GraphViewModel
		@State var currentActiveItem: GraphModel?
		@State var plotWidth: CGFloat = 0

		var body: some View {
				VStack {
						animatedChart()
				}
				.padding(.top, 60)
				.padding(.bottom, 5)
		}

		@ViewBuilder
		func animatedChart() -> some View {
				let max = viewModel.graphData.max { item1, item2 in
						return item2.price > item1.price
				}?.price ?? 0

				let min = viewModel.graphData.max { item1, item2 in
						return item2.price < item1.price
				}?.price ?? 0

				Chart {
						ForEach(viewModel.graphData) { item in
								LineMark(
										x: .value("Day", item.day, unit: .day),
										y: .value("Price", item.animate ? item.price : 0)
								)
								.foregroundStyle(Color.blue.gradient)

								if let currentActiveItem, currentActiveItem.id == item.id {
										RuleMark(x: .value("Day", currentActiveItem.day))
												.lineStyle(.init(lineWidth: 2, miterLimit: 2, dash: [2], dashPhase: 5))
												.offset(x: (plotWidth / CGFloat(viewModel.graphData.count)) / 2)
												.annotation(position: .top) {
														VStack(alignment: .leading, spacing: 6) {
																Text("Price")
																		.font(.caption)
																		.foregroundColor(.gray)

																Text(String(format: "%.2f", NSDecimalNumber(decimal: currentActiveItem.price).doubleValue))
																		.font(.title3.bold())
														}
														.padding(.horizontal, 10)
														.padding(.vertical, 2)
														.background {
																RoundedRectangle(cornerRadius: 10, style: .continuous)
																		.fill(.white.shadow(.drop(radius: 2)))
														}
												}
								}
						}
				}
				.chartYScale(domain: (min)...(max))
				.chartOverlay(content: { proxy in
						GeometryReader {_ in
								Rectangle()
										.fill(.clear).contentShape(Rectangle())
										.gesture(
												DragGesture()
														.onChanged { value in
																let location = value.location
																if let date: Date = proxy.value(atX: location.x) {
																		let calendar = Calendar.current
																		let day = calendar.component(.month, from: date)
																		if let currentItem = viewModel.graphData.first(where: { item in
																				calendar.component(.month, from: item.day) == day
																		}) {
																				self.currentActiveItem = currentItem
																		}
																}
														}.onEnded {_ in
																self.currentActiveItem = nil
														}
										)
						}
				})
				.frame(height: 280)
				.onAppear {
						animateGraph()
				}
		}

		func animateGraph(fromChange: Bool = false) {
				for (index, _) in viewModel.graphData.enumerated() {
						DispatchQueue.main.asyncAfter(deadline: .now() + Double(index) * (fromChange ? 0.03 : 0.05)) {
								withAnimation(fromChange ? .easeInOut(duration: 0.6) : .interactiveSpring(response: 0.8, dampingFraction: 0.8, blendDuration: 0.8)) {
										viewModel.graphData[index].animate = true
								}
						}
				}
		}
}

public struct GraphModel: Identifiable {
		public var id = UUID()
		var day: Date
		var price: Decimal
		var animate = true

		init(point: Point) {
				self.day = point.date
				self.price = point.price
		}
}

