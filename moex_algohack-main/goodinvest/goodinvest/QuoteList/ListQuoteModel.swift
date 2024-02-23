import Foundation
import Combine

public final class ListQuoteModel {
		public enum State {
				case success(quote: [Quote])
				case loading
				case error(error: Error)
			
				var quotes: [Quote] {
						switch self {
								case .success(let quoteList):
										return quoteList
								default:
										return [Quote]()
						}
				}
		}
		@Published public private(set) var state: State
		private var client: QuoteListProvider

		public init(client: QuoteListProvider) {
				self.state = .loading
				self.client = client
				tryGetCetQuotes()
		}

		public func tryGetCetQuotes() {
				self.state = .loading
			
				for i in 0..<3 {
						self.client.quoteList(
								search: .defaultList(2-i),
								completion: { [weak self] result in
										switch result {
										case .success(let quoteList):
												let newQuoteList = quoteList + (self?.state.quotes ?? [Quote]())
												self?.state = .success(quote: newQuoteList)
										case .failure(let error):
												self?.state = .error(error: error) }})
				}
		}
}

