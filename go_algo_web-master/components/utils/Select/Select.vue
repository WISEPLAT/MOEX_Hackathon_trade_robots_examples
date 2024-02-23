<script setup lang="ts">
import {
	Listbox,
	ListboxButton,
	ListboxOptions,
	ListboxOption,
} from "@headlessui/vue";

const emit = defineEmits(["select"]);

const props = defineProps({
	title: String,
	items: Array,
	displayKey: String,
	displayFullSizeKey: {
		type: String,
		default: null,
	},
	isFullSized: {
		type: Boolean,
		default: false,
	},
	description: {
		type: String,
		default: null,
	},
	units: {
		type: String,
		default: null,
	},
});

const selectedItem = ref(props.items[0]);

const handleSelect = () => {
	emit("select", selectedItem.value);
};

onMounted(() => {
	handleSelect();
});
</script>

<template>
	<div
		class="flex flex-col justify-between gap-4 select border-2 hover:border-b-red-400 transition-all rounded-2xl p-4"
	>
		<p class="text-2xl font-bold">{{ title }}</p>
		<p v-if="description" class="opacity-60">{{ description }}</p>
		<div class="flex gap-2 items-end">
			<Listbox v-model="selectedItem" @update:modelValue="handleSelect">
				<div
					:class="isFullSized ? 'full-size' : ''"
					class="relative mt-1"
				>
					<ListboxButton
						v-auto-animate
						class="relative w-full cursor-pointer rounded-lg bg-white py-2 pl-3 pr-10 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm"
					>
						<span class="block truncate" :key="selectedItem">
							{{ selectedItem[displayKey] }}
							<span class="opacity-70" v-if="isFullSized">
								- {{ selectedItem[displayFullSizeKey] }}
							</span>
						</span>
						<span
							class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2"
						>
							<NuxtIcon
								class="nuxt-icon-small"
								name="ui/ic_select"
								alt="Выбрать"
							/>
						</span>
					</ListboxButton>

					<transition
						leave-active-class="transition duration-100 ease-in"
						leave-from-class="opacity-100"
						leave-to-class="opacity-0"
					>
						<ListboxOptions
							class="absolute options mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm"
						>
							<ListboxOption
								v-slot="{ active, selected }"
								v-for="item in items"
								:key="item.id"
								:value="item"
								as="template"
							>
								<li
									:class="[
										active
											? 'transition bg-red-100 text-red-900'
											: 'text-gray-900',
										'relative cursor-pointer p-4 select-none py-2',
									]"
								>
									<span
										:class="[
											selected
												? 'font-bold'
												: 'font-normal',
											'block truncate',
										]"
										>{{ item[displayKey] }}
										<span
											class="opacity-70"
											v-if="isFullSized"
										>
											- {{ item[displayFullSizeKey] }}
										</span>
									</span>
								</li>
							</ListboxOption>
						</ListboxOptions>
					</transition>
				</div>
			</Listbox>
			<p v-if="units">{{ units }}</p>
		</div>
	</div>
</template>

<style>
.options {
	z-index: 10000;
}

.select {
	width: 45%;

	@media (max-width: 400px) {
		width: -webkit-fill-available;
	}
}

.full-size {
	width: -webkit-fill-available;
}
</style>
