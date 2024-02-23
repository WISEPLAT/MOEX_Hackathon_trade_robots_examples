import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {

		var window: UIWindow?
		var coordinator: AppCoordinator?

		func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options connectionOptions: UIScene.ConnectionOptions) {
				guard let windowScene = (scene as? UIWindowScene) else { return }
				let window = UIWindow(windowScene: windowScene)
				coordinator = AppCoordinator(window: window)
				coordinator?.start()
		}

		func sceneDidDisconnect(_ scene: UIScene) {}
		func sceneDidBecomeActive(_ scene: UIScene) {}
		func sceneWillResignActive(_ scene: UIScene) {}
		func sceneWillEnterForeground(_ scene: UIScene) {}
		func sceneDidEnterBackground(_ scene: UIScene) {}

}

