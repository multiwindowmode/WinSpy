package com.example.pair1_imurecorder

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    lateinit var sensorHandler: SensorHandler

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)


        sensorHandler = SensorHandler(this)
        sensorHandler.registerSensors()

        setContent {
            Column {
                SimpleCenterButtonScreen(this@MainActivity)

                Button(modifier = Modifier.height(100.dp).padding(10.dp), onClick = { sensorHandler.setIsRec(true) }) {
                    Text(text = "startRec")
                }
                Button(modifier = Modifier.height(100.dp).padding(10.dp), onClick = { sensorHandler.setIsRec(false) }) {
                    Text(text = "stopRec")
                }
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        sensorHandler.unregisterSensors()
    }
}

@Composable
fun SimpleCenterButtonScreen(mainActivity: MainActivity) {
    var buttonText by remember { mutableStateOf("Click me") }

    Button(modifier = Modifier.height(100.dp).padding(10.dp), onClick = {
        buttonText = "${mainActivity.sensorHandler.writeCounter}, ${mainActivity.sensorHandler.cntpt}"
    }) {
        Text(buttonText)
    }
}
