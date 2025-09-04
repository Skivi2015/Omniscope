package com.omniscope.android

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface OmniScopeApiService {
    @POST("solve")
    fun solve(@Body request: SolveRequest): Call<SolveResponse>
}

data class SolveRequest(
    val bot: String,
    val task: String
)

data class SolveResponse(
    val result: String? = null,
    val transcript: String? = null,
    val error: String? = null
)