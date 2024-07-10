package com.example.tappingimu

import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.tappingimu.ui.theme.ShouJiTheme
import kotlinx.coroutines.delay
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.util.concurrent.atomic.AtomicBoolean
import kotlin.math.roundToInt
import kotlin.random.Random

class SensorThread(mainActivity: MainActivity) : HandlerThread("SensorThread") {
    private var sensorHandler: SensorHandler
    private var handler: Handler

    init {
        start()
        handler = Handler(looper)
        sensorHandler = SensorHandler(mainActivity, handler)
        handler.post { sensorHandler.start() }
    }

    fun cleanUp() {
        handler.post { sensorHandler.stop() }
        quitSafely()
    }

    fun ff() {
        handler.post {sensorHandler.ff() }
    }
}

class MainActivity : ComponentActivity() {

    private lateinit var file: File
    lateinit var bufferedStream: BufferedOutputStream

    private lateinit var sensorThread: SensorThread

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d("tttt", "This function is running on thread: ${Thread.currentThread().name}")

        file = File(this.filesDir, "taps_${fileTimeName}.txt")
        bufferedStream = BufferedOutputStream(FileOutputStream(file, true))

        sensorThread = SensorThread(this)
        setContent {
            ShouJiTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    SensorDataCollector2(this@MainActivity)
                }
            }
        }
    }

    override fun onPause() {
        super.onPause()
        sensorThread.ff()
        bufferedStream.flush()
    }

    override fun onStop() {
        super.onStop()
        sensorThread.ff()
        bufferedStream.flush()
    }

    override fun onDestroy() {
        super.onDestroy()
        sensorThread.cleanUp()
        bufferedStream.flush()
        bufferedStream.close()
    }
}

@Composable
fun SensorDataCollector2(mainActivity: MainActivity) {
    val radiusDp = 50.dp
    val diameterDp = radiusDp * 2
    var widthBox = 0
    var heightBox = 0

    var touchPoint by remember { mutableStateOf(Offset.Zero) }
    var isShowHighlightForTouchPoint by remember { mutableStateOf(false) }
    var indicationPoint by remember { mutableStateOf(Offset.Zero) }
    var isShowIndicationPoint by remember { mutableStateOf(false) }

    Box(modifier = Modifier
        .fillMaxSize()
        .onSizeChanged {
            widthBox = it.width
            heightBox = it.height
            Log.e("asdf1", it.toString())
        }
        .onGloballyPositioned { layoutCoordinates ->
            val position = layoutCoordinates.positionInRoot()
            Log.e("asdf2", "${position.x} ${position.y} ${layoutCoordinates.size}")
        }
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .onGloballyPositioned { layoutCoordinates ->
                    val position = layoutCoordinates.positionInRoot()
                    Log.e("asdf3", "${position.x} ${position.y}")
                }
                .pointerInput(Unit) {
                    detectTapGestures(
                        onPress = {

                            touchPoint = it
                            Log.e("ttttp", "$touchPoint")

                            val sysNano = System.nanoTime()
                            val s = "date = ${getCurrentDateTimeFormatted()}, " +
                                    "timestamp = $sysNano, " +
                                    "x = ${touchPoint.x.toInt()}, " +
                                    "y = ${touchPoint.y.toInt()}\n"

                            mainActivity.bufferedStream.write(s.toByteArray())

                            isShowHighlightForTouchPoint = true
                            isShowIndicationPoint = false

                            tryAwaitRelease()

                            isShowHighlightForTouchPoint = false
                            isShowIndicationPoint = false
                        }
                    )
                }
        ) {
            LaunchedEffect(touchPoint, isShowHighlightForTouchPoint) {
                if (!isShowHighlightForTouchPoint) {
                    delay(1000)
                    indicationPoint = Offset(
                        Random.nextFloat() * widthBox,
                        Random.nextFloat() * heightBox
                    )
                    isShowIndicationPoint = true
                }
            }

            if (isShowHighlightForTouchPoint) {
                Box(
                    modifier = Modifier
                        .offset {
                            IntOffset(
                                (touchPoint.x - radiusDp.toPx()).roundToInt(),
                                (touchPoint.y - radiusDp.toPx()).roundToInt()
                            )
                        }
                        .size(diameterDp) 
                        .background(Color.Red, CircleShape)
                )
                Text("Tapped Point (x = ${touchPoint.x}, y = ${touchPoint.y})", color = Color.Yellow)
            }
            if (isShowIndicationPoint) {
//                Box(
//                    modifier = Modifier
//                        .offset {
//                            IntOffset(
//                                (indicationPoint.x - radiusDp.toPx()).roundToInt(),
//                                (indicationPoint.y - radiusDp.toPx()).roundToInt()
//                            )
//                        }
//                        .size(diameterDp)
//                        .background(Color.Blue, CircleShape)
//                )
                Box(
                    modifier = Modifier
                        .offset {
                            IntOffset(
                                (indicationPoint.x - radiusDp.toPx()).roundToInt(),
                                (indicationPoint.y - radiusDp.toPx()).roundToInt()
                            )
                        }
                        .size(diameterDp)
                        .drawBehind {
                            val radiusPx = radiusDp.toPx()
                            val center = Offset(size.width / 2, size.height / 2)
                            drawCircle(
                                brush = Brush.radialGradient(
                                    colors = listOf(Color.Blue, Color.Transparent),
                                    center = center,
                                    radius = radiusPx
                                ),
                                radius = radiusPx,
                                center = center
                            )
                        }
                )
                Text(
//                    "\nIndicator Coordinates (x = ${indicationPoint.x.toInt()}, y = ${indicationPoint.y.toInt()})",
                    "",
                    color = Color.Black,
                    fontSize = 12.sp
                )
            }
            if (!isShowHighlightForTouchPoint && !isShowIndicationPoint) {
                Text("no touch", color = Color(255, 0, 0))
            }
        }
    }
}