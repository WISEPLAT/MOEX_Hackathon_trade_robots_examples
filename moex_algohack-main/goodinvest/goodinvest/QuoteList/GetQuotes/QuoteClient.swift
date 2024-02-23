import Foundation

public enum ClientError: Error {
		case getRequestError
		case algorithmError
		case decodeJsonError
		case incorrectJsonError
}

let dateFormatter = DateFormatter()

public final class QuoteClient: DetailProvider, ChartsProvider, QuoteListProvider, QuotesStatProvider {
		private let session = URLSession(configuration: URLSessionConfiguration.default)
		private let decoder = JSONDecoder()
		private var urlComponents = URLComponents()
		public init() {
				urlComponents.scheme = "https"
				urlComponents.host = "iss.moex.com"
		}
		public func quoteList(search: SearchForList, completion: @escaping (_: Result<[Quote], Error>) -> Void) {
				let url: URL?
				switch search {
				case let .listByName(searchStr):
						url = URL(string: QuoteClient.Constants.UrlComponentGetListBySearch + "q=" + searchStr)
				case let .defaultList(num):
						url = URL(string: QuoteClient.Constants.UrlComponentGetDefaultList + "start=\(num * 100)")
				}
				guard let url = url else {
						DispatchQueue.main.async {
								completion(.failure(ClientError.algorithmError))
						}
						return
				}
				var request = URLRequest(url: url)
				request.httpMethod = "GET"
				request.timeoutInterval = 20
				let task = session.dataTask(with: request) { data, _, _ in
						guard let data = data else {
								DispatchQueue.main.async {
										completion(.failure(ClientError.getRequestError))
								}
								return
						}
						do {
								let quotesResult = try self.decoder.decode(QuoteListResult.self, from: data)
								DispatchQueue.main.async {
										completion(.success(quotesResult.toQuotes()))
								}
						} catch {
								DispatchQueue.main.async {
										completion(.failure(ClientError.decodeJsonError))
								}
								return
						}
				}
				task.resume()
		}

		public func quoteCharts(
				id: String,
				boardId: String,
				fromDate: Date,
				completion: @escaping (_: Result<QuoteCharts, Error>) -> Void
		) {
				var components = urlComponents
				components.path = "/iss/history/engines/stock/markets/shares/boards/\(boardId)/securities/\(id)/candels.json"
				getChartsAfterDate(array: [],
													 fromDate: fromDate,
													 components: components,
													 start: 0,
													 callback: completion)
		}

		private func getChartsAfterDate(
				array: [Point],
				fromDate: Date,
				components: URLComponents,
				start: Int,
				callback: @escaping (_: Result<QuoteCharts, Error>) -> Void
		) {
				var componentsForURL = components
				componentsForURL.queryItems = [
						URLQueryItem(name: "from", value: "\(String(date: fromDate))"),
						URLQueryItem(name: "start", value: "\(start)"),
				]
				guard let url = componentsForURL.url else {
						DispatchQueue.main.async {
								callback(.failure(ClientError.algorithmError))
						}
						return
				}
				var request = URLRequest(url: url)
				request.httpMethod = "GET"
				request.timeoutInterval = 20
				let task = session.dataTask(with: request) { data, _, _ in
						DispatchQueue.main.async {
								self.obsereDataByGetChartsRequest(
										data: data,
										array: array,
										components: components,
										callback: callback
								)
						}
				}
				task.resume()
		}

		private func obsereDataByGetChartsRequest(
				data: Data?,
				array: [Point],
				components: URLComponents,
				callback: @escaping (_: Result<QuoteCharts, Error>) -> Void
		) {
				guard let data = data else {
						callback(.failure(ClientError.getRequestError))
						return
				}
				do {
						let quoteChartsResult = try decoder.decode(QuoteChartsResult.self, from: data)
						let result = quoteChartsResult.toQuoteCharts()
						switch result {
						case let .success(quoteCharts):
								let points = quoteCharts.points
								var newArray = array
								newArray.append(contentsOf: points)
								if points.count > 1 {
										getChartsAfterDate(
												array: newArray,
												fromDate: points[points.count - 1].date,
												components: components,
												start: 1,
												callback: callback
										)
								} else {
										callback(.success(QuoteCharts(points: newArray)))
								}
						case .failure:
								callback(result)
						}
				} catch {
						callback(.failure(ClientError.decodeJsonError))
				}
		}

		public func quoteDetail(
				id: String,
				boardId: String,
				completion: @escaping (_: Result<QuoteDetail, Error>) -> Void
		) {
				var components = urlComponents
				components.path = "/iss/history/engines/stock/markets/shares/boards/\(boardId)/securities/\(id)/candels.json"
				components.queryItems = [
						URLQueryItem(name: "sort_order", value: "desc"),
				]
				guard let url = components.url else {
						DispatchQueue.main.async {
								completion(.failure(ClientError.algorithmError))
						}
						return
				}
				var request = URLRequest(url: url)
				request.timeoutInterval = 20
				request.httpMethod = "GET"
				let task = session.dataTask(with: request) { data, _, _ in
						guard let data = data else {
								DispatchQueue.main.async {
										completion(.failure(ClientError.getRequestError))
								}
								return
						}
						do {
								let quotCharts = try self.decoder.decode(QuoteChartsResult.self, from: data)
								DispatchQueue.main.async {
										completion(quotCharts.toQuoteDetail())
								}
						} catch {
								DispatchQueue.main.async {
										completion(.failure(ClientError.decodeJsonError))
								}
								return
						}
				}
				task.resume()
		}

		public func quoteStat(
				listOfId: [String],
				listOfBoardId: [String],
				fromDate: Date,
				completion: @escaping (Result<[QuoteCharts?], Error>) -> Void
		) -> QuoteStatToken {
				let quoteStatToken = QuoteStatToken()

				toNextId(
						array: [],
						index: 0,
						quoteStatToken: quoteStatToken,
						lisOfId: listOfId,
						listOfBoardId: listOfBoardId,
						fromDate: fromDate,
						completion: completion)
				return quoteStatToken
		}

		private func toNextId(
				array: [QuoteCharts?],
				index: Int,
				quoteStatToken: QuoteStatToken,
				lisOfId: [String],
				listOfBoardId: [String],
				fromDate: Date,
				completion: @escaping (Result<[QuoteCharts?], Error>) -> Void
		) {
				if index >= lisOfId.count || index >= listOfBoardId.count {
						completion(.failure(ClientError.algorithmError))
				}
				let id = lisOfId[index]
				let boardId = listOfBoardId[index]
				if quoteStatToken.isCanceled {
						return
				}
				quoteCharts(
						id: id,
						boardId: boardId,
						fromDate: fromDate,
						completion: {[weak self] result in
								var newArray = array
								switch result {
								case let .success(quoteCharts):
										newArray.append(quoteCharts)
								case .failure:
										newArray.append(nil)
								}
								if newArray.count == lisOfId.count {
										completion(.success(newArray))
								} else {
										self?.toNextId(
												array: newArray,
												index: index + 1,
												quoteStatToken: quoteStatToken,
												lisOfId: lisOfId,
												listOfBoardId: listOfBoardId,
												fromDate: fromDate,
												completion: completion)
								}
						})
		}
}

private extension QuoteClient {
		enum Constants {
				static let UrlComponentGetListBySearch = "https://iss.moex.com/iss/securities.json?"
				static let UrlComponentGetDefaultList = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/tqbr/securities.json?"
		}
}

private extension String {
		init(date: Date) {
				dateFormatter.dateFormat = "YY-MM-dd"
				self = dateFormatter.string(from: date)
		}
}

