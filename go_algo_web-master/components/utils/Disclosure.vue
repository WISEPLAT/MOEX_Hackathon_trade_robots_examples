<template>
	<div class="w-full opacity-60 hover:opacity-80 transition-all">
		<div class="w-fit max-w-md rounded-2xl bg-white">
			<Disclosure as="div" v-slot="{ open }">
				<DisclosureButton
					:class="
						open ? 'opacity-100 bg-purple-200 text-purple-1000' : ''
					"
					class="flex w-fit justify-between rounded-lg bg-purple-100 px-4 py-2 text-left text-sm font-medium text-purple-900 hover:bg-purple-200 focus:outline-none focus-visible:ring focus-visible:ring-purple-500/75'"
				>
					<span>О параметре</span>
				</DisclosureButton>
				<transition
					enter-active-class="transition duration-300 ease-out"
					enter-from-class="transform scale-95 opacity-0"
					enter-to-class="transform scale-100 opacity-100"
					leave-active-class="transition duration-75 ease-out"
					leave-from-class="transform scale-100 opacity-100"
					leave-to-class="transform scale-95 opacity-0"
				>
					<DisclosurePanel class="pt-4 text-sm text-gray-500">
						{{ disclosureText }}
					</DisclosurePanel>
				</transition>
			</Disclosure>
		</div>
	</div>
</template>

<script setup lang="ts">
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";

const props = defineProps({
	disclosureText: String,
});
</script>
