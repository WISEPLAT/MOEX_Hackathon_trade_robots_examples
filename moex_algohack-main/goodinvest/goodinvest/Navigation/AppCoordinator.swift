import UIKit

class AppCoordinator {
		var childCoordinators = [QuoteCoordinator]()
		let window: UIWindow

		init(window: UIWindow) {
				self.window = window
		}

		func start() {
				let modelQuoteList = ListQuoteModel(client: QuoteClient())
				let quotesVC = QuotesViewController(modelQuoteList: modelQuoteList)
				let quotesNC = UINavigationController(rootViewController: quotesVC)
				quotesVC.didTapButton = { [weak self] quote in
						self?.showQuoteController(with: quote, navigationController: quotesNC)
				}
				
				window.rootViewController = quotesNC
				window.makeKeyAndVisible()
		}

		func showQuoteController(with quote: Quote, navigationController: UINavigationController) {
			 let quoteCoordinator = QuoteCoordinator(navigationController: navigationController, quote: quote)
			 childCoordinators.append(quoteCoordinator)
			 quoteCoordinator.removeFromMemory = { [weak self] in
					 self?.childCoordinators.removeLast()
			 }
			 quoteCoordinator.start()
		}
}
