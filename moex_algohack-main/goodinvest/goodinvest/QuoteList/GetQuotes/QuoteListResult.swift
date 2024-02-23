import Foundation

struct QuoteListResult: Decodable {
		let history: History
		struct History: Decodable {
				let columns: [String]
				let data: [[AnyDecodable]]
		}

		func toQuotes() -> [Quote] {
				var quotes: [Quote] = []
				guard let idQuoteIndex = history.columns.firstIndex(of: QuoteListResult.Constants.idJsonName),
							let nameQuoteIndex = history.columns.firstIndex(of: QuoteListResult.Constants.nameJsonName)
				else {
						return []
				}

				let openPriceQuoteIndex = history.columns.firstIndex(of: QuoteListResult.Constants.openPriceJsonName)
				let closePriceQuoteIndex = history.columns.firstIndex(of: QuoteListResult.Constants.closePriceJsonName)
				for element in history.data {
						if let idQuoteAny = element[safe: idQuoteIndex],
							 let nameQuoteAny = element[safe: nameQuoteIndex] {
								let openPriceQuote = element[safe: openPriceQuoteIndex ?? -1]
								let closePriceQuote = element[safe: closePriceQuoteIndex ?? -1]
								if let idQuote = idQuoteAny.getStringValue(),
									 let nameQuote = nameQuoteAny.getStringValue() {
										quotes.append(
												Quote(id: idQuote,
															name: nameQuote,
															openPrice: openPriceQuote?.getDecimalValue(),
															closePrice: closePriceQuote?.getDecimalValue()))
								}
						}
				}
				return quotes
		}
}

private extension QuoteListResult {
		enum Constants {
				static let idJsonName = "SECID"
				static let nameJsonName = "SHORTNAME"
				static let openPriceJsonName = "OPEN"
				static let closePriceJsonName = "CLOSE"
		}
}

extension Collection {
		subscript(safe index: Index) -> Element? {
				indices.contains(index) ? self[index] : nil
		}
}
