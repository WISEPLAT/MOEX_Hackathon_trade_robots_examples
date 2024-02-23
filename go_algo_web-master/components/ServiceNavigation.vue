<script setup lang="ts"></script>

<template>
	<nav>
		<ul
			class="flex bg-opacity-90 text-white rounded-2xl flex-row gap-4 w-fit bg-black p-6"
		>
			<li>
				<NuxtLink to="/service/mark-up/all">Разметка</NuxtLink>
			</li>
			<li>
				<NuxtLink to="/service/dataset/all">Дата-сеты</NuxtLink>
			</li>
			<li>
				<NuxtLink to="/service/neural-learning/all"
					>Обучение сети
				</NuxtLink>
			</li>
			<li>
				<NuxtLink to="/service/back-testing/all">Бек-тесты </NuxtLink>
			</li>
			<li>
				<NuxtLink to="/service/signals/all">Сигналы</NuxtLink>
			</li>
		</ul>
	</nav>
</template>

<style scoped lang="scss">
a {
	border-radius: 42px;
	padding: 12px;
	border: 1px solid #6e6e6e;
	opacity: 0.7;
	background: #262626;

	transition: 0.3s;
	&:hover {
		opacity: 1;
	}
}

@media (max-width: 800px) {
	ul {
		flex-wrap: wrap;
		row-gap: 2rem;
	}
}
</style>
