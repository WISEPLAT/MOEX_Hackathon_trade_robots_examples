import UIKit
import SwiftUI

class QuoteDetailView: UIView {

		private let buttonView: TimeIntervalsControl = {
				let control = TimeIntervalsControl(
						intervals: labels,
						selectedSegmentIndex: QuoteDetailModel.defaultInterval.rawValue
						)
				control.translatesAutoresizingMaskIntoConstraints = false
				return control
		}()

		private let lastDateTextLabel = UILabel()
		private let lastDateLabel = UILabel()

		private let closePriceLabel = UILabel()
		private let closePriceAmountLabel = UILabel()

		private let openPriceLabel = UILabel()
		private let openPriceAmountLabel = UILabel()

		private let averagePriceLabel = UILabel()
		private let averagePriceAmountLabel = UILabel()

		private let mainStackView = UIStackView()
		let detailLabelsStackView = UIStackView()
		private let dateStackView = UIStackView()
		private let openPriceStackView = UIStackView()
		private let closePriceStackView = UIStackView()
		private let averagePriceStackView = UIStackView()
		var timeIntervalSelectionHandler: ((QuoteDetailModel.Interval) -> Void)?

	
	// MARK: todo predict
		private let addToFavsButton: UIButton = {
				var button = UIButton()
				button.backgroundColor = Theme.Colors.button
				button.translatesAutoresizingMaskIntoConstraints = false
				button.layer.cornerRadius = Theme.StyleElements.buttonCornerRadius
				button.setTitle("Predict price", for: .normal)
				button.setTitleColor(Theme.Colors.buttonText, for: .normal)
				button.setTitleColor(Theme.Colors.buttonHighlightedText, for: .highlighted)
				button.setTitleColor(Theme.Colors.buttonHighlightedText, for: .disabled)
				button.titleLabel?.font = Theme.Fonts.button
				button.titleLabel?.adjustsFontForContentSizeCategory = true
				//button.addTarget(self, action: #selector(addToFavoritesTapped(_:)), for: .touchUpInside)
				button.setTitle("Predict is not available", for: .disabled)
				return button
		}()

		init() {
				super.init(frame: .zero)
				translatesAutoresizingMaskIntoConstraints = false

				setupUI()
				setupLayout()

				buttonView.delegate = self
		}

		@available(*, unavailable)
		required init?(coder _: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		private func setupUI() {
				applyStyleForLabel(for: lastDateTextLabel, text: "Date")
				applyStyleForLabel(for: closePriceLabel, text: "Close price")
				applyStyleForLabel(for: openPriceLabel, text: "Open price")
				applyStyleForLabel(for: averagePriceLabel, text: "Average price")
				applyStyleForAmountLabel(for: lastDateLabel, text: "10.10.1010")
				applyStyleForAmountLabel(for: closePriceAmountLabel, text: "1000 $")
				applyStyleForAmountLabel(for: openPriceAmountLabel, text: "1000 $")
				applyStyleForAmountLabel(for: averagePriceAmountLabel, text: "1000 $")
		}

		private func setupLayout() {
				arrangeStackView(
						for: dateStackView,
						subviews: [lastDateTextLabel, lastDateLabel]
				)
				arrangeStackView(
						for: closePriceStackView,
						subviews: [closePriceLabel, closePriceAmountLabel]
				)
				arrangeStackView(
						for: openPriceStackView,
						subviews: [openPriceLabel, openPriceAmountLabel]
				)
				arrangeStackView(
						for: averagePriceStackView,
						subviews: [averagePriceLabel, averagePriceAmountLabel]
				)
				arrangeStackView(
						for: detailLabelsStackView,
						subviews: [dateStackView,
											 closePriceStackView,
											 openPriceStackView,
											 averagePriceStackView],
						spacing: Theme.Layout.smallSpacing,
						axis: .vertical
				)
				arrangeStackView(
						for: mainStackView,
						subviews: [buttonView,
											 detailLabelsStackView,
											 addToFavsButton],
						spacing: Theme.Layout.bigSpacing,
						axis: .vertical
				)
				setContentHuggingPriorities()
				addSubview(mainStackView)
				NSLayoutConstraint.activate([
						buttonView.heightAnchor.constraint(equalToConstant: 40),
						addToFavsButton.heightAnchor.constraint(equalToConstant: Theme.Layout.buttonHeight),
						mainStackView.topAnchor.constraint(equalTo: topAnchor),
						mainStackView.trailingAnchor.constraint(equalTo: trailingAnchor),
						mainStackView.leadingAnchor.constraint(equalTo: leadingAnchor),

				])
		}

		private func setContentHuggingPriorities() {
				averagePriceLabel.setContentHuggingPriority(.defaultHigh, for: .horizontal)
				averagePriceAmountLabel.setContentHuggingPriority(.defaultLow, for: .horizontal)
				openPriceLabel.setContentHuggingPriority(.defaultHigh, for: .horizontal)
				openPriceAmountLabel.setContentHuggingPriority(.defaultLow, for: .horizontal)
				closePriceLabel.setContentHuggingPriority(.defaultHigh, for: .horizontal)
				closePriceAmountLabel.setContentHuggingPriority(.defaultLow, for: .horizontal)
				lastDateTextLabel.setContentHuggingPriority(.defaultHigh, for: .horizontal)
				lastDateLabel.setContentHuggingPriority(.defaultLow, for: .horizontal)
		}
}

// MARK: - Apply style to UI Elements

private extension QuoteDetailView {
		func applyStyleForLabel(
				for label: UILabel,
				text: String) {
						label.text = text
						label.font = Theme.Fonts.subtitle
				}

		func applyStyleForAmountLabel(
				for label: UILabel,
				text: String) {
						label.text = text
						label.textAlignment = .right
						label.font = Theme.Fonts.title
				}

		func arrangeStackView(
				for stackView: UIStackView,
				subviews: [UIView],
				spacing: CGFloat = 0,
				axis: NSLayoutConstraint.Axis = .horizontal,
				distribution: UIStackView.Distribution = .fill,
				aligment: UIStackView.Alignment = .fill
		) {
				stackView.axis = axis
				stackView.spacing = spacing
				stackView.distribution = distribution
				stackView.alignment = aligment
				stackView.translatesAutoresizingMaskIntoConstraints = false
				subviews.forEach { item in stackView.addArrangedSubview(item)
				}
		}
}

extension QuoteDetailView: TimeIntervalControlDelgate {
		func timeIntervalControlDidChangeSelected() {
				guard let selectionHandel = timeIntervalSelectionHandler else {
						return
				}
				selectionHandel(QuoteDetailModel.Interval(rawValue: buttonView.selectedSegmentIndex)!)
		}
}

extension QuoteDetailView {
		static var labels: [String] {
				var result = [String]()
				QuoteDetailModel.Interval.allCases.forEach { interval in
						result.append(interval.label)
				}
				return result
		}

		func setDetailsData(quoteDetailData: QuoteDetail?) {
				guard let quoteDetailData else {
						closePriceAmountLabel.text = "-"
						openPriceAmountLabel.text = "-"
						averagePriceAmountLabel.text = "-"
						lastDateLabel.text = "-"
						return
				}
				closePriceAmountLabel.text = "\(getRoundedValue(quoteDetailData.closePrice))"
				openPriceAmountLabel.text = "\(getRoundedValue(quoteDetailData.openPrice))"
				averagePriceAmountLabel.text = "\(getRoundedValue(quoteDetailData.currentPrice))"
				let dateFormatter = DateFormatter()
				dateFormatter.dateFormat = "dd.MM.YYYY"
				lastDateLabel.text = dateFormatter.string(from: quoteDetailData.date)
		}

		func getRoundedValue(_ number: Decimal, symbolNumber: Int = 4) -> Decimal {
				var localCopy = number
				var rounded = Decimal()
				NSDecimalRound(&rounded, &localCopy, 4, .plain)
				return rounded
		}
}

extension QuoteDetailView {
		func disableButton() {
				addToFavsButton.isEnabled = false
		}

		func enableButton() {
				addToFavsButton.isEnabled = true
		}
}

