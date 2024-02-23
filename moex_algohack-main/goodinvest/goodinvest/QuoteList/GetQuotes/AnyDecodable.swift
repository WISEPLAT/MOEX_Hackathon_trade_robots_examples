import Foundation

struct AnyDecodable: Decodable {
		var value: Any?

		private struct CodingKeys: CodingKey {
				var stringValue: String
				var intValue: Int?
				init?(intValue: Int) {
						stringValue = "\(intValue)"
						self.intValue = intValue
				}

				init?(stringValue: String) { self.stringValue = stringValue }
		}

		func getIntValue() -> Int? {
				value as? Int
		}

		func getStringValue() -> String? {
				value as? String
		}

		func getDoubleValue() -> Double? {
				value as? Double
		}

		func getDecimalValue() -> Decimal? {
				value as? Decimal
		}

		init(from decoder: Decoder) throws {
				if let container = try? decoder.container(keyedBy: CodingKeys.self) {
						var result = [String: Any]()
						try container.allKeys.forEach { key throws in
								result[key.stringValue] = try container.decode(AnyDecodable.self, forKey: key).value
						}
						value = result
				} else if var container = try? decoder.unkeyedContainer() {
						var result = [Any?]()
						while !container.isAtEnd {
								try result.append(container.decode(AnyDecodable.self).value)
						}
						value = result
				} else if let container = try? decoder.singleValueContainer() {
						if let intVal = try? container.decode(Int.self) {
								value = intVal
						} else if let doubleVal = try? container.decode(Decimal.self) {
								value = doubleVal
						} else if let boolVal = try? container.decode(Bool.self) {
								value = boolVal
						} else if let stringVal = try? container.decode(String.self) {
								value = stringVal
						} else {
								value = nil
						}
				} else {
						throw DecodingError.dataCorrupted(
								DecodingError.Context(codingPath: decoder.codingPath, debugDescription: "Could not serialise"))
				}
		}
}
