<template>
	<footer
		class="flex flex-col gap-6 bg-black bg-opacity-90 text-white bottom-0 left-0 right-0 shrink-0"
	>
		<AppLogo />
		<div class="opacity-80">
			<p>
				Платформа по построению торговых и инвестиционных стратегий с
				искусственным интеллектом на основе данных AlgoPack
			</p>
			<p>Решение разработано в рамках Хакатона GO.ALGO</p>
		</div>
		<div class="flex gap-4">
			<IconedLink
				title="Страница хакатона"
				navigate-to="https://goalgo.ru/"
			/>
			<IconedLink
				title="Мастер-репозиторий"
				navigate-to="https://github.com/DaniilVdovin/GO.ALGO.Neuro"
			/>
		</div>
	</footer>
</template>
<script setup lang="ts"></script>
