export function formatDate(date: Date): string {
    return date.toLocaleString("ru", { year: "numeric", month: "long", day: "2-digit" });
}
