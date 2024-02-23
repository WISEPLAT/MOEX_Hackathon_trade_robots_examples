import UIKit
import Combine

public class QuotesViewController: UIViewController {
		public var didTapButton: ((Quote) -> Void)?
		private var animationPlayed = true
		private var arrayToShow: [Quote] = []
		private let modelQuoteList: ListQuoteModel
		private lazy var tableView = UITableView()
		private let searchController = UISearchController()
		private var state: ListQuoteModel.State {
				didSet {
						applyData()
				}
		}

		private lazy var errorView: ErrorViewForDetails = {
				let view = ErrorViewForDetails()
				view.tryAgainHandler = { [weak self] in
						self?.modelQuoteList.tryGetCetQuotes()
				}
				return view
		}()

		private var observations = Set<AnyCancellable>()
		public init(modelQuoteList: ListQuoteModel) {
				self.modelQuoteList = modelQuoteList
				state = .loading
				super.init(nibName: nil, bundle: nil)
		}

		required init?(coder: NSCoder) {
				fatalError("init(coder:) has not been implemented")
		}

		override public func viewDidLayoutSubviews() {
				super.viewDidLayoutSubviews()
				tableView.alpha = 1
		}

		override public func viewDidLoad() {
				super.viewDidLoad()
				configureTitle()
				configureTableView()
				if animationPlayed {
						tableView.alpha = 0
				}
				self.modelQuoteList.$state.sink(receiveValue: { state in
						self.state = state
				})
				.store(in: &observations)
		}
		private func applyData() {
				self.showFullQuotes()
				self.tableView.reloadData()
				self.animateTableView()
				self.animationPlayed = false
		}

		private func configureTitle() {
				title = "Quotes"
				navigationItem.searchController = searchController
				searchController.searchResultsUpdater = self
				searchController.obscuresBackgroundDuringPresentation = false
		}

		private func showFullQuotes() {
				switch state {
				case .success(let quotes):
						errorView.removeFromSuperview()
						let filteredData = quotes.filter { isFull($0) } + quotes.filter { !isFull($0) }
								arrayToShow = filteredData
				case .error:
						errorView.layoutErrorView(superView: view)
						// MARK: - page with error information/ignore
				case .loading: break
				}
		}

		private func isFull(_ q: Quote) -> Bool {
				q.openPrice != nil && q.closePrice != nil
		}

		private func animateTableView() {
				tableView.reloadData()

				let cells = tableView.visibleCells

				let tableViewHeight = tableView.bounds.size.height

				for cell in cells {
						cell.transform = CGAffineTransform(translationX: 0, y: tableViewHeight)
				}

				var delayCounter = 0
				for cell in cells {
						UIView.animate(withDuration: 1.75,
													 delay: Double(delayCounter) * 0.05,
													 usingSpringWithDamping: 0.8,
													 initialSpringVelocity: 0,
													 options: .curveEaseOut,
													 animations: { cell.transform = CGAffineTransform.identity }, completion: nil)
						delayCounter += 1
				}
		}

		private func configureTableView() {
				view.addSubview(tableView)
				setTableViewDelegates()
				tableView.rowHeight = 90
				tableView.register(QuoteCustomCell.self, forCellReuseIdentifier: "QuoteCustomCell")

				tableView.translatesAutoresizingMaskIntoConstraints = false
				NSLayoutConstraint.activate([
						tableView.topAnchor.constraint(equalTo: view.topAnchor),
						tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
						tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
						tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor),
				])
		}

		private func setTableViewDelegates() {
				tableView.delegate = self
				tableView.dataSource = self
				searchController.searchBar.delegate = self
		}
}

extension QuotesViewController: UITableViewDataSource, UITableViewDelegate {
		public func tableView(_: UITableView, numberOfRowsInSection _: Int) -> Int {
				arrayToShow.count
		}

		public func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
				let cell = tableView.dequeueReusableCell(withIdentifier: "QuoteCustomCell") as! QuoteCustomCell
				cell.setData(model: arrayToShow[indexPath.row])
				return cell
		}

		public func tableView(_: UITableView, didSelectRowAt indexPath: IndexPath) {
				didTapButton?(arrayToShow[indexPath.row])
		}
}

extension QuotesViewController: UISearchResultsUpdating, UISearchBarDelegate {
		public func updateSearchResults(for searchController: UISearchController) {
				guard let text = searchController.searchBar.text?.uppercased() else {
						return
				}
				guard !text.isEmpty else {
						return
				}
				switch state {
				case .success(let quotes):
						var filteredData = quotes.filter { $0.name.uppercased().contains(text) || $0.id.uppercased().contains(text) }
						filteredData = filteredData.filter { isFull($0) } + filteredData.filter { !isFull($0) }
						arrayToShow = filteredData
				case .error: break
						// MARK: - page with error information/ignore
				case .loading: break
						// MARK: - page with error information/ignore
				}
				tableView.reloadData()
		}
		public func searchBarCancelButtonClicked(_ searchBar: UISearchBar) {
				switch state {
				case .success(let quotes):
						let filteredData = quotes.filter { isFull($0) } + quotes.filter { !isFull($0) }
						arrayToShow = filteredData
				case .error: break
						// MARK: - page with error information/ignore
				case .loading: break
						// MARK: - page with error information/ignore
				}
				tableView.reloadData()
		}
}
