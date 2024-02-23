<script setup lang="ts"></script>

<template>
	<header class="flex flex-row gap-4 items-center">
		<AppLogo />
		<nav>
			<ul class="flex gap-4 font-bold">
				<li>
					<HeaderItem navigate-to="/" title="Главная" />
				</li>
			</ul>
		</nav>
	</header>
</template>

<style scoped>
header {
	@media (max-width: 450px) {
		flex-direction: column;
		align-items: start;
	}
}
</style>
