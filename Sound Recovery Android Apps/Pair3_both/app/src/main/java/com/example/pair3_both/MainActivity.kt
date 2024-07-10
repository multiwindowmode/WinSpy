package com.example.pair3_both

import android.media.MediaPlayer
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.pair3_both.ui.theme.Pair3_bothTheme

class MainActivity : ComponentActivity() {

    private var mediaPlayer: MediaPlayer? = null
    lateinit var sensorHandler: SensorHandler

    override fun onCreate(savedInstanceState: Bundle?) {

        sensorHandler = SensorHandler(this)
        sensorHandler.registerSensors()

        super.onCreate(savedInstanceState)

        setContent {

            Column {
                Pair3_bothTheme {
                    AudioList()
                }
                SimpleCenterButtonScreen(this@MainActivity)
                Row {
                    Button(
                        modifier = Modifier.height(100.dp).padding(10.dp),
                        onClick = { sensorHandler.setIsRec(true) }) {
                        Text(text = "startRec")
                    }
                    Button(
                        modifier = Modifier.height(100.dp).padding(10.dp),
                        onClick = { sensorHandler.setIsRec(false) }) {
                        Text(text = "stopRec")
                    }
                }
            }
        }
    }

    @Composable
    fun AudioList() {
        val audioFiles = listOf(
//            "a054",
//            "a326",
//            "a689",
//            "a725",
//            "a893",
//            "a967",
            "a314159",
            "a476149",
            "a704288",
            "a895331",
            "a923424",
            "a951413",
            "all2"
        )

        LazyColumn {
            items(audioFiles) { audioFile ->
                AudioItem(audioFile)
            }
        }
    }

    @Composable
    fun AudioItem(audioFile: String) {
        Card(
            modifier = Modifier
                .clickable { playAudio(audioFile) }
                .fillMaxWidth(),
        ) {
            Column(
                modifier = Modifier.padding(16.dp).padding(10.dp)
            ) {
                Text(text = audioFile)
            }
        }
    }

    private fun playAudio(audioName: String) {
        val resourceId = resources.getIdentifier(audioName, "raw", packageName)
        releaseMediaPlayer()
        mediaPlayer = MediaPlayer.create(this, resourceId)
        mediaPlayer?.start()
    }

    private fun releaseMediaPlayer() {
        mediaPlayer?.release()
        mediaPlayer = null
    }

    override fun onDestroy() {
        super.onDestroy()
        releaseMediaPlayer()
        sensorHandler.unregisterSensors()
    }
}

@Composable
fun SimpleCenterButtonScreen(mainActivity: MainActivity) {
    var buttonText by remember { mutableStateOf("Click me to log rate") }

    Button(modifier = Modifier.height(100.dp).padding(10.dp), onClick = {
        buttonText = "${mainActivity.sensorHandler.writeCounter}, ${mainActivity.sensorHandler.cntpt}"
    }) {
        Text(buttonText)
    }
}
