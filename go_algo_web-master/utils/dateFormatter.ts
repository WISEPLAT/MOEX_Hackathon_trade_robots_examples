const options = { year: "numeric", month: "long", day: "numeric" };

export function formatDate(date: string) {
	const dateObject = new Date(date);

	return dateObject.toLocaleDateString("ru-RU", options);
}
