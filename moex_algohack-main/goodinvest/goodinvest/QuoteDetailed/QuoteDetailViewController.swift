import UIKit
import SwiftUI
import Combine

enum DetailState {
		case loading
		case error
		case success
}
enum QuoteDetailViewState {
		case loading
		case error
		case success
}

public class QuoteDetailViewController: UIViewController {
		private var quoteDetailClient: DetailProvider? = QuoteClient()
		private var chartDataClient: ChartsProvider? = QuoteClient()
		private var graphData: QuoteCharts?
		private var detailsData: QuoteDetail?
		private let quote: Quote
		public var onViewDidDisappear: (() -> Void)?
		private let quoteDetailModel: QuoteDetailModel
		private var observations = Set<AnyCancellable>()

		private lazy var errorView: ErrorViewForDetails = {
				let view = ErrorViewForDetails()
				view.isHidden = true
				view.tryAgainHandler = { [weak self] in
						self?.getQuoteData()
				}
				return view
		}()

		private lazy var quoteDetailView: QuoteDetailView = {
				let view = QuoteDetailView()
				view.timeIntervalSelectionHandler = { interval in
						self.quoteDetailModel.selectedInterval = interval

				}
				return view
		}()

		private let graphViewModel = GraphViewModel()

		private lazy var graphView: UIHostingController<GraphView> = {
				let graphView = GraphView(viewModel: graphViewModel)
				let hostingController = UIHostingController(rootView: graphView)
				hostingController.view.translatesAutoresizingMaskIntoConstraints = false
				return hostingController
		}()

		private var graphLoadingIndicator: UIActivityIndicatorView?

		private lazy var quoteDetailMainStackView: UIStackView = {
				var stack = UIStackView(arrangedSubviews: [graphView.view, quoteDetailView])
				stack.spacing = Theme.Layout.bigSpacing
				stack.axis = .vertical
				let graphLoadingIndicator = UIActivityIndicatorView(style: .large)
				graphLoadingIndicator.translatesAutoresizingMaskIntoConstraints = false
				graphView.view.addSubview(graphLoadingIndicator)
				self.graphLoadingIndicator = graphLoadingIndicator
				NSLayoutConstraint.activate([
						graphView.view.centerXAnchor.constraint(equalTo: graphLoadingIndicator.centerXAnchor),
						graphView.view.centerYAnchor.constraint(equalTo: graphLoadingIndicator.centerYAnchor),
				])
				return stack
		}()

		public init(quote: Quote) {
				self.quote = quote
				quoteDetailModel = QuoteDetailModel(id: quote.id, boardId: "TQBR")

				super.init(nibName: nil, bundle: nil)
		}

		required init?(coder: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		private var viewState: QuoteDetailViewState? {
				didSet {
						switch viewState {
						case .loading:
								errorView.isHidden = true
						case .success:
								errorView.isHidden = true
								quoteDetailView.setDetailsData(quoteDetailData: detailsData)
						case .error:
								errorView.isHidden = false
								errorView.layoutErrorView(superView: view)
						case .none:
								break
						}
				}
		}

		private var detailState: DetailState? {
				didSet {
						updateViewState(graphState: quoteDetailModel.state, detailState: detailState)
				}
		}

		override public func viewDidLoad() {
				super.viewDidLoad()
				setupUI()
				getQuoteData()
				setupLayout()
				addChild(graphView)
				graphView.didMove(toParent: self)

				self.quoteDetailModel.$state.sink(receiveValue: { state in
						self.updateViewState(graphState: state, detailState: self.detailState)
						self.updateGraphLoadingState(isLoading: state == .loading)
				})
				.store(in: &observations)

				self.quoteDetailModel.$points.sink(receiveValue: { points in
						self.graphViewModel.graphData = points.map { GraphModel(point: $0) }
				})
				.store(in: &observations)

		}

		func setupUI() {
				view.backgroundColor = Theme.Colors.background
				quoteDetailMainStackView.translatesAutoresizingMaskIntoConstraints = false
				updateButton()
				view.addSubview(quoteDetailMainStackView)
				view.addSubview(errorView)
		}

		private func setupLayout() {
				NSLayoutConstraint.activate([
						graphView.view.heightAnchor.constraint(equalToConstant: 300),
						quoteDetailMainStackView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: Theme.Layout.topOffset),
						quoteDetailMainStackView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: Theme.Layout.sideOffset),
						quoteDetailMainStackView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -Theme.Layout.sideOffset),
						quoteDetailMainStackView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
				])
		}

		private func updateGraphLoadingState(isLoading: Bool) {
				if isLoading {
						graphLoadingIndicator?.startAnimating()
				} else {
						graphLoadingIndicator?.stopAnimating()
				}
				graphLoadingIndicator?.isHidden = !isLoading
		}

		private func updateViewState(graphState: QuoteDetailModel.State, detailState: DetailState?) {
				switch detailState {
				case (.loading):
						viewState = .loading
				case .error:
						viewState = .error
				default:
						viewState = .success
				}
		}

		func layoutErrorView() {
				NSLayoutConstraint.activate([
						errorView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: Theme.Layout.topOffset),
						errorView.leadingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.leadingAnchor, constant: Theme.Layout.sideOffset),
						errorView.trailingAnchor.constraint(equalTo: view.safeAreaLayoutGuide.trailingAnchor, constant: -Theme.Layout.sideOffset),
						errorView.bottomAnchor.constraint(equalTo: view.safeAreaLayoutGuide.bottomAnchor)
				])
		}
}

// MARK: - Work with client
private extension QuoteDetailViewController {
		func getQuoteData() {
				getDataForDetails()
		}

		func getDataForDetails() {
				detailState = .loading
				quoteDetailClient?.quoteDetail(id: quote.id , boardId: "tqbr") { [weak self] result in
						switch result {
						case .success(let quoteDetail):
								self?.detailsData = quoteDetail
								self?.detailState = .success
						case .failure(let error):
								let customError = error as! ClientError
								self?.errorView.updateErrorLabel(error: customError)
								self?.detailState = .error
						}
				}
		}

}

private extension QuoteDetailViewController {
		func getDate() -> Date {
				let date = Calendar.current.date(byAdding: .year, value: -1, to: .now)
				return date!
		}
}

extension QuoteDetailViewController {
		func updateButton() {
				if availableCompanies.contains(detailsData?.name ?? " ") {
						quoteDetailView.enableButton()
				} else {
						quoteDetailView.disableButton()
				}
		}
}

extension QuoteDetailViewController {
		override public func viewDidDisappear(_ animated: Bool) {
				super.viewDidDisappear(animated)
				onViewDidDisappear?()
		}
}

let availableCompanies: [String] = [
		"GAZP", "TATN"
]
