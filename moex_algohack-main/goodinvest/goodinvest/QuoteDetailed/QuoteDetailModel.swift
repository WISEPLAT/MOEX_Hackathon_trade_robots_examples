import Foundation

final class QuoteDetailModel {

		private var id: String
		private var boardId: String
		private let client: ChartsProvider = QuoteClient()

		@Published
		private(set) var points = [Point]()
		private var cachePoints = [Point]()

		@Published
		private(set) var state: State

		static let defaultInterval: Interval = .threeMounts
		private var cachedInterval: Interval?
		var selectedInterval: Interval {
				didSet {
						self.updatePoints()
				}
		}

		private static func getDate(byAdding: Calendar.Component, value: Int) -> Date {
				let date = Calendar.current.date(byAdding: byAdding, value: value, to: .now)
				return date!
		}

		init(
				id: String = Constants.defaultId,
				boardId: String = Constants.boardId
		) {
				self.points = []
				self.cachePoints = []
				self.id = id
				self.boardId = boardId
				self.state = .loading
				self.selectedInterval = QuoteDetailModel.defaultInterval
				updatePoints()
		}

		private func checkIfUpdatePointsNedeed() -> Bool {
				if self.cachedInterval == nil {
						return true
				}
				if let interval = self.cachedInterval, selectedInterval.rawValue > interval.rawValue {
						return true
				}
				 return false
		}

		private func updatePoints() {
				if checkIfUpdatePointsNedeed() {
						state = .loading
						cachedInterval = selectedInterval
						client.quoteCharts(
								id: self.id,
								boardId: self.boardId,
								fromDate: selectedInterval.fromDate,
								completion: {
										[weak self] result in
										guard let self else { return }
										switch result {
										case .success(let graphData):
												self.cachePoints = graphData.points
												self.updateGraphPoints()
												self.state = .success
										case .failure:
												self.cachePoints = []
												self.updateGraphPoints()
												self.state = .error
										}
								}
						)
				} else {
						updateGraphPoints()
				}
		}

		private func updateGraphPoints() {
				points = cachePoints.filter({ $0.date >= selectedInterval.fromDate })
		}
}

extension QuoteDetailModel {
		enum Interval: Int, CaseIterable {
				case oneDay
				case threeDays
				case sevenDays
				case oneMounth
				case threeMounts
				case oneYear
				case twoYear

				var fromDate: Date {
						switch self {
								case .oneDay:
										return getDate(byAdding: .day, value: -1)
								case .threeDays:
										return getDate(byAdding: .day, value: -3)
								case .sevenDays:
										return getDate(byAdding: .day, value: -7)
								case .oneMounth:
										return getDate(byAdding: .month, value: -1)
								case .threeMounts:
										return getDate(byAdding: .month, value: -3)
								case .oneYear:
										return getDate(byAdding: .year, value: -1)
								case .twoYear:
										return getDate(byAdding: .year, value: -2)
						}
				}

				var label: String {
						switch self {
								case .oneDay:
										return "1D"
								case .threeDays:
										return "3D"
								case .sevenDays:
										return "7D"
								case .oneMounth:
										return "1M"
								case .threeMounts:
										return "3M"
								case .oneYear:
										return "1Y"
								case .twoYear:
										return "2Y"
						}
				}
		}

		enum State {
				case loading
				case success
				case error
		}
}

extension QuoteDetailModel {
		private struct Constants {
				static let defaultId = "ABRD"
				static let boardId = "tqbr"
		}
}

