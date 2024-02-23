import UIKit

final class QuoteCustomCell: UITableViewCell {
		private let shortNameLabel = UILabel()
		private let fullNameLabel = UILabel()
		private let priceLabel = UILabel()
		private let diffPriceLabel = UILabel()
		private let diffPercentLabel = UILabel()
		private let namesStackView = UIStackView()
		private let leadingStackView = UIStackView()
		private let trailingStackView = UIStackView()

		override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
				super.init(style: style, reuseIdentifier: reuseIdentifier)
				configureStacks()
				configureShortNameLabel()
				configureFullNameLabel()
				configurePriceLabel()
				configureDiffPriceLabel()
				configurePercentLabel()
				self.selectionStyle = .none
		}

		@available(*, unavailable)
		required init?(coder _: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		private func configureStacks() {
				configureDiffStackView()
				configureNamesStackView()
				configureNamePriceStackView()
		}

		private func configureStackView(stackView: UIStackView,
																		axis: NSLayoutConstraint.Axis,
																		aligment: UIStackView.Alignment,
																		distribution: UIStackView.Distribution,
																		spacing: CGFloat,
																		viewsArray: [UIView],
																		isInContentView: Bool) {
				stackView.axis = axis
				stackView.alignment = aligment
				stackView.distribution = distribution
				stackView.spacing = spacing
				viewsArray.forEach { stackView.addArrangedSubview($0) }
				if isInContentView {
						contentView.addSubview(stackView) }
				}

		private func configureDiffStackView() {
				configureStackView(stackView: trailingStackView,
													 axis: .vertical,
													 aligment: .fill,
													 distribution: .fillEqually,
													 spacing: 10,
													 viewsArray: [diffPercentLabel, diffPriceLabel],
													 isInContentView: true)

				trailingStackView.translatesAutoresizingMaskIntoConstraints = false
				diffPercentLabel.translatesAutoresizingMaskIntoConstraints = false
				NSLayoutConstraint.activate([
						trailingStackView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
						trailingStackView.trailingAnchor.constraint(equalTo: contentView.trailingAnchor, constant: -16),
						trailingStackView.widthAnchor.constraint(equalToConstant: 80),
				])

		}

		private func configureNamesStackView() {
				configureStackView(stackView: namesStackView,
													 axis: .vertical,
													 aligment: .fill,
													 distribution: .fill,
													 spacing: 10,
													 viewsArray: [shortNameLabel, fullNameLabel],
													 isInContentView: false)
		}

		private func configureNamePriceStackView() {
				configureStackView(stackView: leadingStackView,
													 axis: .horizontal,
													 aligment: .fill,
													 distribution: .fill,
													 spacing: 0,
													 viewsArray: [namesStackView, priceLabel],
													 isInContentView: true)

				leadingStackView.translatesAutoresizingMaskIntoConstraints = false
				NSLayoutConstraint.activate([
						leadingStackView.centerYAnchor.constraint(equalTo: contentView.centerYAnchor),
						leadingStackView.leadingAnchor.constraint(equalTo: contentView.leadingAnchor, constant: 16),
						leadingStackView.trailingAnchor.constraint(equalTo: trailingStackView.leadingAnchor, constant: -30)
				])
				setPriorities()
		}

		private func setPriorities() {
				shortNameLabel.setContentCompressionResistancePriority(UILayoutPriority.defaultHigh,
																															 for: .horizontal)
				fullNameLabel.setContentCompressionResistancePriority(UILayoutPriority.defaultLow,
																															for: .horizontal)
		}

		private func configureShortNameLabel() {
				shortNameLabel.numberOfLines = 1
				shortNameLabel.font = Theme.Fonts.title
		}

		private func configureFullNameLabel() {
				fullNameLabel.numberOfLines = 1
				fullNameLabel.font = Theme.Fonts.subtitle
				fullNameLabel.textColor = Theme.Colors.subLabelText
		}

		private func configurePriceLabel() {
				priceLabel.numberOfLines = 1
				priceLabel.font = Theme.Fonts.title
				priceLabel.textAlignment = .right
		}

		private func configurePercentLabel() {
				diffPercentLabel.textAlignment = .right
				diffPercentLabel.textColor = Theme.Colors.labelText
		}

		private func configureDiffPriceLabel() {
				diffPriceLabel.font = Theme.Fonts.subtitle
				diffPriceLabel.textAlignment = .right
				diffPriceLabel.translatesAutoresizingMaskIntoConstraints = false
				diffPriceLabel.heightAnchor.constraint(equalToConstant: 30).isActive = true
		}

		func setData(model: Quote) {
				shortNameLabel.text = model.id
				fullNameLabel.text = model.name
				if let openPrice = model.openPrice, let closePrice = model.closePrice {
						let diff = openPrice - closePrice
						priceLabel.text = "₽\(closePrice.rounded(2, .plain))"
						diffPriceLabel.text = "\(diff.rounded(5, .plain))"
						let percent = (diff / openPrice) * 100
						if diff < 0 {
								diffPercentLabel.text = "\(percent.rounded(2, .plain))%"
								diffPercentLabel.textColor = Theme.Colors.redBackground
						} else {
								diffPercentLabel.text = "+\(percent.rounded(2, .plain))%"
								diffPercentLabel.textColor = Theme.Colors.greenBackground
						}
				} else {
						priceLabel.textColor = Theme.Colors.mainText
						diffPercentLabel.textColor = Theme.Colors.mainText
						diffPriceLabel.textColor = Theme.Colors.mainText
						priceLabel.text = "₽---"
						diffPercentLabel.text = "---%"
						diffPriceLabel.text = "---"
				}
		}
}

extension Decimal {
		func rounded(_ scale: Int, _ roundingMode: NSDecimalNumber.RoundingMode) -> Decimal {
				var result = Decimal()
				var localCopy = self
				NSDecimalRound(&result, &localCopy, scale, roundingMode)
				return result
		}
}

