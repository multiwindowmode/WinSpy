package com.example.pair2_speaker

import android.media.MediaPlayer
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Card
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.clickable
import androidx.compose.material3.Button


class MainActivity : ComponentActivity() {
    private var mediaPlayer: MediaPlayer? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                AudioList()
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
            "all2",
            "all280"
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
                modifier = Modifier.padding(16.dp)
            ) {
                Text(text = audioFile)
            }
        }
    }

    private fun playAudio(audioName: String) {
        Thread.sleep(500)
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
    }

    @Preview(showBackground = true)
    @Composable
    fun DefaultPreview() {
        MaterialTheme {
            AudioList()
        }
    }
}