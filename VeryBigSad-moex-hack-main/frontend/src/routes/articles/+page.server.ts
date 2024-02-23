import { articles } from '$lib/articles.server';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    return { articles: articles() };
};
