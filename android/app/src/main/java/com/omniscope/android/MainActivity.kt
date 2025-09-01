package com.omniscope.android

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class MainActivity : AppCompatActivity() {
    
    private lateinit var editTextTask: EditText
    private lateinit var buttonSolve: Button
    private lateinit var buttonDiagnostics: Button
    private lateinit var textViewResult: TextView
    private lateinit var apiService: OmniScopeApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        initViews()
        setupApiService()
        setupClickListeners()
    }
    
    private fun initViews() {
        editTextTask = findViewById(R.id.editTextTask)
        buttonSolve = findViewById(R.id.buttonSolve)
        buttonDiagnostics = findViewById(R.id.buttonDiagnostics)
        textViewResult = findViewById(R.id.textViewResult)
    }
    
    private fun setupApiService() {
        apiService = ApiClient.getInstance().create(OmniScopeApiService::class.java)
    }
    
    private fun setupClickListeners() {
        buttonSolve.setOnClickListener {
            val task = editTextTask.text.toString()
            if (task.isNotEmpty()) {
                solveTask(task)
            }
        }
        
        buttonDiagnostics.setOnClickListener {
            val intent = Intent(this, DiagnosticsActivity::class.java)
            startActivity(intent)
        }
    }
    
    private fun solveTask(task: String) {
        val request = SolveRequest(bot = "scouty", task = task)
        
        apiService.solve(request).enqueue(object : Callback<SolveResponse> {
            override fun onResponse(call: Call<SolveResponse>, response: Response<SolveResponse>) {
                if (response.isSuccessful) {
                    val result = response.body()
                    textViewResult.text = result?.result ?: "No result"
                } else {
                    textViewResult.text = "Error: ${response.code()}"
                }
            }
            
            override fun onFailure(call: Call<SolveResponse>, t: Throwable) {
                textViewResult.text = "Network error: ${t.message}"
            }
        })
    }
}