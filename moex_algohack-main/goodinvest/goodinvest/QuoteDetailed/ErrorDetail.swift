import UIKit

public class ErrorViewForDetails: UIView {
		public typealias RetryHandler = () -> Void

		public var tryAgainHandler: RetryHandler?

		private let errorLabel: UILabel = {
				let label = UILabel()
				label.font = Theme.Fonts.error
				label.textColor = Theme.Colors.mainText
				label.text = "Error occured"
				label.translatesAutoresizingMaskIntoConstraints = false
				return label
		}()

		public func layoutErrorView(superView: UIView) {
				superView.addSubview(self)
				self.backgroundColor = .systemBackground
				NSLayoutConstraint.activate([
						self.topAnchor.constraint(equalTo: superView.safeAreaLayoutGuide.topAnchor, constant: Theme.Layout.topOffset),
						self.leadingAnchor.constraint(equalTo: superView.safeAreaLayoutGuide.leadingAnchor, constant: Theme.Layout.sideOffset),
						self.trailingAnchor.constraint(equalTo: superView.safeAreaLayoutGuide.trailingAnchor, constant: -Theme.Layout.sideOffset),
						self.bottomAnchor.constraint(equalTo: superView.safeAreaLayoutGuide.bottomAnchor)
				])
		}

		private lazy var tryAgainButton: UIButton = {
				let button = UIButton()
				button.backgroundColor = Theme.Colors.button
				button.layer.cornerRadius = Theme.StyleElements.buttonCornerRadius
				button.setTitle("Try again", for: .normal)
				button.titleLabel?.font = Theme.Fonts.button
				button.setTitleColor(Theme.Colors.buttonText, for: .normal)
				button.setTitleColor(Theme.Colors.buttonHighlightedText, for: .highlighted)
				button.translatesAutoresizingMaskIntoConstraints = false
				button.addTarget(self, action: #selector(tryAgainButtonTapped(_:)), for: .touchUpInside)
				return button
		}()

		private let errorStackView: UIStackView = {
				let stackView = UIStackView()
				stackView.translatesAutoresizingMaskIntoConstraints = false
				stackView.axis = .vertical
				stackView.spacing = Theme.Layout.bigSpacing
				return stackView
		}()

		public init() {
				super.init(frame: .zero)
				self.backgroundColor = Theme.Colors.background
				self.translatesAutoresizingMaskIntoConstraints = false
				setupLayout()
		}

		required init?(coder: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		private func setupLayout() {
				errorStackView.addArrangedSubview(errorLabel)
				errorStackView.addArrangedSubview(tryAgainButton)
				self.addSubview(errorStackView)
				NSLayoutConstraint.activate([
						tryAgainButton.heightAnchor.constraint(equalToConstant: Theme.Layout.buttonHeight),
						errorStackView.centerXAnchor.constraint(equalTo: self.centerXAnchor),
						errorStackView.centerYAnchor.constraint(equalTo: self.centerYAnchor)
				])
		}
}

extension ErrorViewForDetails {
		@objc
		private func tryAgainButtonTapped(_ sender: UIButton) {
				tryAgainHandler?()
		}

		public func updateErrorLabel(error: ClientError) {
				switch error {
				case .algorithmError:
						fallthrough
				case .decodeJsonError:
						fallthrough
				case .incorrectJsonError:
						errorLabel.text = "Data is unreachable"
				case .getRequestError:
						errorLabel.text = "No internet connection"
				}
		}
}
