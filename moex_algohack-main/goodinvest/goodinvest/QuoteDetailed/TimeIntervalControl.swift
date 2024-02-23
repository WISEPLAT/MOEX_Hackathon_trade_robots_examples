import UIKit

class TimeIntervalsControl: UIView {

		weak var delegate: TimeIntervalControlDelgate?

		var selectedSegmentIndex: Int {
				didSet {
						updateSegments(
								selectedSegmentIndex: selectedSegmentIndex,
								oldSelectedSegmentIndex: oldValue
						)
				}
		}

		private var selectedSegmentConstraint: NSLayoutConstraint!
		private var segments = [UIButton]()

		private let selectorView: UIView = {
				let view = UIView()
				view.layer.cornerRadius = Constants.cornerRadius
				view.backgroundColor = Constants.selectedBackgroundColor
				view.translatesAutoresizingMaskIntoConstraints = false
				return view
		}()

		private let stackView: UIStackView = {
				let stackView = UIStackView()
				stackView.axis = .horizontal
				stackView.alignment = .center
				stackView.distribution = .equalCentering
				stackView.translatesAutoresizingMaskIntoConstraints = false
				return stackView
		}()

		init(
				intervals: [String],
				selectedSegmentIndex: Int = Constants.defaultSelectedSegmentIndex
		) {
				if selectedSegmentIndex >= intervals.count || selectedSegmentIndex < 0 {
						self.selectedSegmentIndex = Constants.defaultSelectedSegmentIndex
				} else {
						self.selectedSegmentIndex = selectedSegmentIndex
				}
				super.init(frame: .zero)
				setupLayout()
				setupUI(intervals: intervals)
		}

		@available(*, unavailable)
		required init? (coder _: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		private func setupLayout() {
				backgroundColor = .clear
				addSubview(selectorView)
				addSubview(stackView)
		}

		private func setupUI(intervals: [String]) {
				for (index, interval) in intervals.enumerated() {
						let button = UIButton(
								title: interval,
								titleColor: Constants.defaultTitleColor,
								backgroundColor: Constants.defaultBackgroundColor,
								borderColor: Constants.defaultBorderColor,
								cornerRadius: Constants.cornerRadius,
								borderWidth: Constants.borderWidth,
								sizeFont: Constants.sizeFont
						)

						if index == selectedSegmentIndex {
							button.setTitleColor(Constants.selectTitleColor, for: .normal)
								button.layer.borderColor = Constants.selectedBorderColor.cgColor
								button.backgroundColor = Constants.selectedBackgroundColor
						}

						segments.append(button)
						stackView.addArrangedSubview(button)
						button.tag = index
						button.addTarget(self, action: #selector(buttonTapped(button:)), for: .touchUpInside)

						NSLayoutConstraint.activate([
								button.heightAnchor.constraint(equalTo: stackView.heightAnchor),
								button.widthAnchor.constraint(equalTo: stackView.heightAnchor),
						])
				}

				selectedSegmentConstraint = selectorView.centerXAnchor.constraint(
						equalTo: segments[selectedSegmentIndex].centerXAnchor
				)
				NSLayoutConstraint.activate([
						selectorView.centerYAnchor.constraint(equalTo: segments[selectedSegmentIndex].centerYAnchor),
						selectedSegmentConstraint,
						selectorView.heightAnchor.constraint(equalTo: segments[selectedSegmentIndex].heightAnchor),
						selectorView.widthAnchor.constraint(equalTo: segments[selectedSegmentIndex].widthAnchor),
						stackView.widthAnchor.constraint(equalTo: widthAnchor),
						stackView.heightAnchor.constraint(equalTo: heightAnchor),
				])
		}

		private func updateSegments(selectedSegmentIndex: Int, oldSelectedSegmentIndex: Int) {
				delegate?.timeIntervalControlDidChangeSelected()
				segments.forEach { button in
						button.isSelected = false
				}

				segments[selectedSegmentIndex].isSelected.toggle()
				selectedSegmentConstraint.isActive = false
				selectedSegmentConstraint = selectorView.centerXAnchor.constraint(
						equalTo: segments[selectedSegmentIndex].centerXAnchor
				)
				selectedSegmentConstraint.isActive = true
				UIView.animate(
						withDuration: 0.2,
						delay: 0,
						options: .curveEaseOut,
						animations: {
								self.segments[oldSelectedSegmentIndex].backgroundColor = Constants.defaultBackgroundColor
								self.segments[oldSelectedSegmentIndex].layer.borderColor = Constants.defaultBorderColor.cgColor
								self.segments[oldSelectedSegmentIndex].setTitleColor(Constants.defaultTitleColor, for: .normal)
								self.segments[selectedSegmentIndex].backgroundColor = Constants.selectedBackgroundColor
								self.segments[selectedSegmentIndex].layer.borderColor = Constants.selectedBorderColor.cgColor
								self.segments[selectedSegmentIndex].setTitleColor(Constants.selectTitleColor, for: .normal)
								self.layoutIfNeeded()
						}, completion: { _ in
								UIImpactFeedbackGenerator(style: .light).impactOccurred()
						}
				)
		}
}

extension TimeIntervalsControl {
		@objc
		private func buttonTapped(button: UIButton) {
				selectedSegmentIndex = button.tag
		}
}

private extension TimeIntervalsControl {
		enum Constants {
				static let defaultSelectedSegmentIndex = 0
				static let selectedBorderColor = Theme.Colors.button
				static let defaultBorderColor = Theme.Colors.borderColor
				static let selectedBackgroundColor = Theme.Colors.button
				static let defaultBackgroundColor = UIColor.clear
				static let selectTitleColor = Theme.Colors.buttonText
				static let defaultTitleColor = Theme.Colors.button
				static let cornerRadius: CGFloat = Theme.StyleElements.timeIntervalButtonCornerRadius
				static let borderWidth: CGFloat = 0.5
				static let sizeFont: CGFloat = 13
		}
}

private extension UIButton {
		convenience init(
				title: String,
				titleColor: UIColor,
				backgroundColor: UIColor,
				borderColor: UIColor,
				cornerRadius: CGFloat,
				borderWidth: CGFloat,
				sizeFont: CGFloat
		) {
				self.init(frame: .zero)
				setTitle(title, for: .normal)
				setTitleColor(titleColor, for: .normal)
				self.backgroundColor = backgroundColor
				layer.borderColor = borderColor.cgColor
				layer.borderWidth = borderWidth
				layer.cornerRadius = cornerRadius
				titleLabel?.font = .systemFont(ofSize: sizeFont)
				translatesAutoresizingMaskIntoConstraints = false
		}
}

protocol TimeIntervalControlDelgate: AnyObject {
		func timeIntervalControlDidChangeSelected()
}
