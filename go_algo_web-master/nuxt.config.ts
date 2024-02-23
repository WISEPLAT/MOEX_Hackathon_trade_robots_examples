export default defineNuxtConfig({
	devtools: { enabled: true },
	runtimeConfig: {
		public: {
			apiRoot: "https://goalgoneuro.tw1.su/api/v1/",
		},
	},
	css: [
		"~/assets/css/main.css",
		"~/assets/css/general.scss",
		"~/assets/css/special.css",
		"~/assets/css/fonts.css",
		"~/assets/css/navigation.css",
		"~/assets/css/animations.css",
		"~/assets/css/icons.css",
		"~/assets/css/responsive.css",
	],
	postcss: {
		plugins: {
			tailwindcss: {},
			autoprefixer: {},
		},
	},
	components: [
		{
			path: "~/components",
			pathPrefix: false,
		},
	],
	modules: [
		"nuxt-headlessui",
		"nuxt-icons",
		"@pinia/nuxt",
		"@formkit/auto-animate/nuxt",
	],
	build: {
		transpile: ["tslib"],
	},
});
