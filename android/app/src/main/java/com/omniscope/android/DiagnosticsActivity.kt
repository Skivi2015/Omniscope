package com.omniscope.android

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class DiagnosticsActivity : AppCompatActivity() {
    
    private lateinit var buttonRunDiagnostics: Button
    private lateinit var textViewDiagnosticsResult: TextView
    private lateinit var apiService: OmniScopeApiService

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_diagnostics)
        
        initViews()
        setupApiService()
        setupClickListeners()
    }
    
    private fun initViews() {
        buttonRunDiagnostics = findViewById(R.id.buttonRunDiagnostics)
        textViewDiagnosticsResult = findViewById(R.id.textViewDiagnosticsResult)
    }
    
    private fun setupApiService() {
        apiService = ApiClient.getInstance().create(OmniScopeApiService::class.java)
    }
    
    private fun setupClickListeners() {
        buttonRunDiagnostics.setOnClickListener {
            runDiagnostics()
        }
    }
    
    private fun runDiagnostics() {
        val diagnosticsBuilder = StringBuilder()
        
        // Test basic math
        testBasicMath(diagnosticsBuilder)
        
        // Test HTTP call
        testHttpCall(diagnosticsBuilder)
        
        // Test JSON parsing
        testJsonParsing(diagnosticsBuilder)
    }
    
    private fun testBasicMath(diagnosticsBuilder: StringBuilder) {
        val request = SolveRequest(bot = "scouty", task = "python result = 2 + 3")
        
        apiService.solve(request).enqueue(object : Callback<SolveResponse> {
            override fun onResponse(call: Call<SolveResponse>, response: Response<SolveResponse>) {
                if (response.isSuccessful && response.body()?.result?.contains("5") == true) {
                    diagnosticsBuilder.append("✓ Basic Math: PASS\n")
                } else {
                    diagnosticsBuilder.append("✗ Basic Math: FAIL\n")
                }
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
            
            override fun onFailure(call: Call<SolveResponse>, t: Throwable) {
                diagnosticsBuilder.append("✗ Basic Math: ERROR - ${t.message}\n")
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
        })
    }
    
    private fun testHttpCall(diagnosticsBuilder: StringBuilder) {
        val request = SolveRequest(bot = "scouty", task = "fetch https://httpbin.org/json and json parse")
        
        apiService.solve(request).enqueue(object : Callback<SolveResponse> {
            override fun onResponse(call: Call<SolveResponse>, response: Response<SolveResponse>) {
                if (response.isSuccessful && response.body()?.transcript?.isNotEmpty() == true) {
                    diagnosticsBuilder.append("✓ HTTP Call: PASS\n")
                } else {
                    diagnosticsBuilder.append("✗ HTTP Call: FAIL\n")
                }
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
            
            override fun onFailure(call: Call<SolveResponse>, t: Throwable) {
                diagnosticsBuilder.append("✗ HTTP Call: ERROR - ${t.message}\n")
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
        })
    }
    
    private fun testJsonParsing(diagnosticsBuilder: StringBuilder) {
        val request = SolveRequest(bot = "scouty", task = "json {\"test\": \"value\"}")
        
        apiService.solve(request).enqueue(object : Callback<SolveResponse> {
            override fun onResponse(call: Call<SolveResponse>, response: Response<SolveResponse>) {
                if (response.isSuccessful && response.body()?.result?.contains("test") == true) {
                    diagnosticsBuilder.append("✓ JSON Parsing: PASS\n")
                } else {
                    diagnosticsBuilder.append("✗ JSON Parsing: FAIL\n")
                }
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
            
            override fun onFailure(call: Call<SolveResponse>, t: Throwable) {
                diagnosticsBuilder.append("✗ JSON Parsing: ERROR - ${t.message}\n")
                updateDiagnosticsDisplay(diagnosticsBuilder.toString())
            }
        })
    }
    
    private fun updateDiagnosticsDisplay(result: String) {
        runOnUiThread {
            textViewDiagnosticsResult.text = result
        }
    }
}