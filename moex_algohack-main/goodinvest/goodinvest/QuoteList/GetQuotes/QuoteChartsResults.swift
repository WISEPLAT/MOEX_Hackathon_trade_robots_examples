import Foundation

struct QuoteChartsResult: Decodable {
		let history: History
		struct History: Decodable {
				let columns: [String]
				let data: [[AnyDecodable]]
		}

		func toQuoteCharts() -> Result<QuoteCharts, Error> {
				var poinst: [Point] = []
				guard let dateIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.dateJsonName),
							let priceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.priceJsonName),
							let openPriceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.openJsonName),
							let closePriceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.closeJsonName)
				else {
						return .failure(ClientError.incorrectJsonError)
				}

				for element in history.data {
						if let dateAny = element[safe: dateIndex],
							 let priceAny = element[safe: priceIndex],
							 let openPriceAny = element[safe: openPriceIndex],
							 let closePriceAny = element[safe: closePriceIndex] {
								if let date = dateFromString(str: dateAny.getStringValue()),
									 let price = priceAny.getDecimalValue(),
									 let openPrice = openPriceAny.getDecimalValue(),
									 let closePrice = closePriceAny.getDecimalValue() {
										poinst.append(Point(date, price, openPrice, closePrice))
								}
						}
				}
				return .success(QuoteCharts(points: poinst))
		}

		func toQuoteDetail() -> Result<QuoteDetail, Error> {
				guard let dateIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.dateJsonName),
							let priceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.priceJsonName),
							let openPriceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.openJsonName),
							let closePriceIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.closeJsonName),
							let nameIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.nameJsonName),
							let idIndex = history.columns.firstIndex(of: QuoteChartsResult.Constants.idJsonName)
				else {
						return .failure(ClientError.incorrectJsonError)
				}
				for element in history.data {
						if let dateAny = element[safe: dateIndex],
							 let priceAny = element[safe: priceIndex],
							 let openPriceAny = element[safe: openPriceIndex],
							 let closePriceAny = element[safe: closePriceIndex],
							 let nameAny = element[safe: nameIndex],
							 let idAny = element[safe: idIndex] {
								if let id = idAny.getStringValue(),
									 let name = nameAny.getStringValue(),
									 let date = dateFromString(str: dateAny.getStringValue()),
									 let price = priceAny.getDecimalValue(),
									 let openPrice = openPriceAny.getDecimalValue(),
									 let closePrice = closePriceAny.getDecimalValue() {
										return .success(QuoteDetail(id: id,
																								name: name,
																								openPrice: openPrice,
																								currentPrice: price,
																								closePrice: closePrice,
																								date: date))
								}
						} else {
								return .failure(ClientError.decodeJsonError)
						}
				}
				return .failure(ClientError.incorrectJsonError)
		}
}

private extension QuoteChartsResult {
		enum Constants {
				static let nameJsonName = "SHORTNAME"
				static let closeJsonName = "CLOSE"
				static let openJsonName = "OPEN"
				static let idJsonName = "SECID"
				static let dateJsonName = "TRADEDATE"
				static let priceJsonName = "WAPRICE"
		}

		func dateFromString(str: String?) -> Date? {
				guard let str = str else {
						return nil
				}
				let dateFormatter = DateFormatter()
				dateFormatter.dateFormat = "yyyy'-'MM'-'dd'"
				return dateFormatter.date(from: str)
		}
}
