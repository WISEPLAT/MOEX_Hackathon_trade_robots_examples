import Foundation

public protocol ChartsProvider {
		func quoteCharts(
				id: String,
				boardId: String,
				fromDate: Date,
				completion: @escaping (Result<QuoteCharts, Error>) -> Void
		)
}

public protocol DetailProvider {
		func quoteDetail(
				id: String,
				boardId: String,
				completion: @escaping (Result<QuoteDetail, Error>) -> Void
		)
}

public enum SearchForList {
		case listByName(String)
		case defaultList(Int)
}

public protocol QuoteListProvider {
		func quoteList(
				search: SearchForList,
				completion: @escaping (Result<[Quote], Error>) -> Void
		)
}

public struct Quote {
		public let id: String
		public let name: String
		public let openPrice: Decimal?
		public let closePrice: Decimal?

		public init(
				id: String,
				name: String,
				openPrice: Decimal?,
				closePrice: Decimal?
		) {
				self.id = id
				self.name = name
				self.openPrice = openPrice
				self.closePrice = closePrice
		}
}

public typealias Point = (date: Date, price: Decimal, openPrice: Decimal, closePrice: Decimal)

public struct QuoteCharts {
		public var points: [Point]

		public init(
				points: [Point]
		) {
				self.points = points
		}
}

public struct QuoteDetail {
		public let id: String
		public let name: String
		public let openPrice: Decimal
		public let currentPrice: Decimal
		public let closePrice: Decimal
		public let date: Date

		public init(
				id: String,
				name: String,
				openPrice: Decimal,
				currentPrice: Decimal,
				closePrice: Decimal,
				date: Date
		) {
				self.id = id
				self.name = name
				self.openPrice = openPrice
				self.currentPrice = currentPrice
				self.closePrice = closePrice
				self.date = date
		}
}

public protocol QuotesStatProvider {
		func quoteStat(
				listOfId: [String],
				listOfBoardId: [String],
				fromDate: Date,
				completion: @escaping (Result<[QuoteCharts?], Error>) -> Void
		) -> QuoteStatToken
}

public final class QuoteStatToken {
		public init() {}
		public private(set) var isCanceled = false
		public func cancel() {
				isCanceled = true
		}
}
