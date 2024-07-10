package com.example.tappingimu10

import android.content.Context
import android.os.Bundle
import android.os.Handler
import android.os.HandlerThread
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
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
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.layout.positionInRoot
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import com.example.tappingimu10.ui.theme.TappingImu10Theme
import kotlinx.coroutines.delay
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import kotlin.math.abs
import kotlin.math.roundToInt
import kotlin.random.Random

// honor not expand
val xl = 0
val xr = 1060
val yl = 1353
val yr = 2167
val dx = (xr - xl) / 3
val dy = (yr - yl) / 4

//val xl = 0
//val xr = 2156
//val yl = 1362
//val yr = 2167
//val dx = (xr - xl) / 3
//val dy = (yr - yl) / 4

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
        handler.post { sensorHandler.ff() }
    }
}

class MainActivity : ComponentActivity() {


    private lateinit var file: File
    lateinit var bufferedStream: BufferedOutputStream

    private lateinit var sensorThread: SensorThread

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.i("asdfdxdy", "$dx $dy")
        Log.d("tttt", "This function is running on thread: ${Thread.currentThread().name}")

        file = File(this.filesDir, "taps_${fileTimeName}.txt")
        bufferedStream = BufferedOutputStream(FileOutputStream(file, true))

        if (false) {
            val f = File(this.filesDir, "test_test.txt")
            val b = BufferedOutputStream(FileOutputStream(f, true))
            var _s = "x"
            while (_s.length < 200) {
                _s += _s
            }
            _s += '\n'
            for (i in 0..(5000 * 500)) {
                b.write(_s.toByteArray())
            }
            b.flush()
            b.close()
        }

        sensorThread = SensorThread(this)
        setContent {
            TappingImu10Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background
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

fun getWhichChar(px: Int, py: Int): Char {
    if ((px in xl until xr) && (py in yl until yr)) {
        val g: Int = px / dx
        val h: Int = (py - yl) / dy
        Log.i("asdf", "g = $g, h = $h")
        val s = "123456789.0d";
        val idx = h * 3 + g;
        if (idx in s.indices) {
            return s[idx]
        }
    }
    return 'x'
}

@Composable
fun SensorDataCollector2(mainActivity: MainActivity) {
    var touchPoint by remember { mutableStateOf(Offset.Zero) }
    var isShowHighlightForTouchPoint by remember { mutableStateOf(false) }

    var indicationPoint by remember { mutableStateOf(IntOffset.Zero) }
    var isShowIndicationPoint by remember { mutableStateOf(false) }

    val backgroundImage = painterResource(id = R.drawable.num_board)

    Box(modifier = Modifier
        .fillMaxSize()
        .onGloballyPositioned { layoutCoordinates ->
            val position = layoutCoordinates.positionInRoot()
            Log.i("asdf2", "${position.x} ${position.y}")

            // w * h = 1060 * 2157 -> without top 100 and bottom ?
            Log.i("asdf2", "${layoutCoordinates.size}")
        }) {

        Image(
            painter = backgroundImage,
            contentDescription = "Background Image",
            modifier = Modifier.fillMaxSize(),
            contentScale = ContentScale.FillBounds
//            contentScale = ContentScale.Crop
        )

        Box(modifier = Modifier
            .fillMaxSize()
            .onGloballyPositioned { layoutCoordinates ->
                val position = layoutCoordinates.positionInRoot()
                Log.i("asdf3", "${position.x} ${position.y} ${layoutCoordinates.size}")
            }
            .pointerInput(Unit) {
                detectTapGestures(onPress = {

                    touchPoint = it
                    Log.i("ttttp", "$touchPoint")

                    val sysNano = System.nanoTime()
                    val s = "date = ${getCurrentDateTimeFormatted()}, " + "timestamp = $sysNano, " +
                            "x = ${touchPoint.x.toInt()}, " + "y = ${touchPoint.y.toInt()}, " +
                            "which = ${
                                getWhichChar(
                                    touchPoint.x.toInt(),
                                    touchPoint.y.toInt()
                                )
                            }" + "\n"

                    Log.i("asdf", s)

                    mainActivity.bufferedStream.write(s.toByteArray())

                    isShowHighlightForTouchPoint = true
                    isShowIndicationPoint = false

                    tryAwaitRelease()

                    isShowHighlightForTouchPoint = false
                    isShowIndicationPoint = false
                })
            }) {
            LaunchedEffect(touchPoint, isShowHighlightForTouchPoint) {
                if (!isShowHighlightForTouchPoint) {
                    delay(1000)
                    val indicationPointIdx = abs(Random.nextInt()) % 12
                    Log.i("asdfIndIdx", "$indicationPointIdx")
                    val g = indicationPointIdx % 3
                    val h = indicationPointIdx / 3
                    indicationPoint = IntOffset(g * dx, yl + h * dy)
                    isShowIndicationPoint = true
                }
            }
            if (isShowHighlightForTouchPoint) {
                val radiusDp = 35.dp
                val diameterDp = radiusDp * 2
                Box(modifier = Modifier
                    .offset {
                        IntOffset(
                            (touchPoint.x - radiusDp.toPx()).roundToInt(),
                            (touchPoint.y - radiusDp.toPx()).roundToInt()
                        )
                    }
                    .size(diameterDp)
                    .background(Color.Blue, CircleShape)
                )
                Text("\nTouch Point: x: ${touchPoint.x}, y: ${touchPoint.y}", color = Color.Green)
            }
            if (isShowIndicationPoint) {
                val radiusDp = 40.dp
                val diameterDp = radiusDp * 2
                Log.i("asdf", "$indicationPoint")
//                Box(modifier = Modifier
//                    .offset {
//                        IntOffset(
//                            (indicationPoint.x + dx / 2 - radiusDp.toPx()).roundToInt(),
//                            (indicationPoint.y + dy / 2 - radiusDp.toPx()).roundToInt()
//                        )
//                    }
//                    .size(diameterDp)
//                    .background(Color.Green, CircleShape)
//                )
                Box(
                    modifier = Modifier
                        .offset {
                            IntOffset(
                                (indicationPoint.x + dx / 2 - radiusDp.toPx()).roundToInt(),
                                (indicationPoint.y + dy / 2 - radiusDp.toPx()).roundToInt()
                            )
                        }
                        .size(diameterDp)
                        .drawBehind {
                            val radiusPx = radiusDp.toPx()
                            val center = Offset(size.width / 2, size.height / 2)
                            drawCircle(
                                brush = Brush.radialGradient(
//                                    colors = listOf(Color.Green, Color.Transparent),
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
//                    "Indication Point Idx: ${indicationPoint}}",
                    "",
                    color = Color.Black
                )
            }
            if (!isShowHighlightForTouchPoint && !isShowIndicationPoint) {
                Text("\nNo Touch", color = Color.Green)
            }
        }
    }
}