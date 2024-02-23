<script setup>
import { vAutoAnimate } from "@formkit/auto-animate";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";

const props = defineProps({
	firstTabTitle: String,
	secondTabTitle: String,
});
</script>

<template>
	<TabGroup class="flex flex-col gap-4">
		<TabList class="flex gap-4">
			<Tab as="template" v-slot="{ selected }">
				<button
					:class="{
						'bg-green-600 text-white': selected,
						'bg-green-100 text-black': !selected,
					}"
				>
					{{ firstTabTitle }}
				</button>
			</Tab>
			<Tab as="template" v-slot="{ selected }">
				<button
					:class="{
						'bg-green-400 text-white': selected,
						'bg-green-100 text-black': !selected,
					}"
				>
					{{ secondTabTitle }}
				</button>
			</Tab>
		</TabList>
		<TabPanels v-auto-animate>
			<TabPanel key="tab1">
				<slot name="tab1"></slot>
			</TabPanel>
			<TabPanel key="tab2">
				<slot name="tab2"></slot>
			</TabPanel>
		</TabPanels>
	</TabGroup>
</template>

<style scoped lang="scss">
button {
	border: 1px solid rgba(0, 0, 0, 0);

	&:hover {
		border: 1px solid rgba(0, 0, 0, 0.4);
	}
}
</style>
