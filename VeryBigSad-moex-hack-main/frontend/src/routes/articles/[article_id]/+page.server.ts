import { article as get_article, headers as get_headers } from '$lib/articles.server';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params }) => {
    let article = get_article(params.article_id);
    let headers = get_headers(params.article_id);
    return { article, headers };
};
