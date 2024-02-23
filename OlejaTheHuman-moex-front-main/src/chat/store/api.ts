import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import {DatasetMessageI, MessageI} from './types';
import {BASE_API_PATH} from '../../consts';

export const apiSlice = createApi({
    reducerPath: 'apiSlice',
    baseQuery: fetchBaseQuery({
        baseUrl: BASE_API_PATH,
    }),
    tagTypes: ['Get'],
    endpoints: (builder) => ({
        postMessage: builder.mutation({
            query: (payload: DatasetMessageI) => ({
                url: `/dataset_chat?dataset_id=${payload.dataset_id}&user_query=${payload.user_query}`,
                method: 'GET',
                headers: {
                    'Content-type': 'application/json; charset=UTF-8',
                },
            }),
            invalidatesTags: ['Get'],
        }),
    }),
})
export const {usePostMessageMutation} = apiSlice