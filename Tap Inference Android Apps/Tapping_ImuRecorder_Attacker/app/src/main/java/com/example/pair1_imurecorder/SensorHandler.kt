package com.example.pair1_imurecorder

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.SystemClock
import android.util.Log
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.util.concurrent.atomic.AtomicBoolean

internal object SensorEventTimeConverter {
    private val bootTimeMillis: Long = System.currentTimeMillis() - SystemClock.elapsedRealtime()

    fun convertTimestampToReadable(timestampNanos: Long): String {
        val eventTimeMillis = bootTimeMillis + timestampNanos / 1_000_000

        val eventTimeInstant = Instant.ofEpochMilli(eventTimeMillis)
        val formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS").withZone(ZoneId.systemDefault())

        return formatter.format(eventTimeInstant)
    }
}

class SensorHandler(private val context1: Context) : SensorEventListener {

    private var sensorManager: SensorManager = context1.getSystemService(Context.SENSOR_SERVICE) as SensorManager
    private var accelerometer: Sensor? = null

    private var t0: Long = 0L // time_begin
    private var onSensorChangedCounter: Long = 0L // sensor event count
    var cntpt: Double = 0.0 // sensor event count / (time_now - time_begin)

    var writeCounter = 0L // the tiem num writed in the file
    private var stopCounter = 0L // count on pair<startRec, stopRec>

    private var isRec: AtomicBoolean = AtomicBoolean(false)
    private val w = ArrayList<Pair<SensorEvent, Long>>()

    init {
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
    }

    fun setIsRec(boolean: Boolean) {
        if (boolean) {
            isRec.set(true)
        } else {
            isRec.set(false)
            CoroutineScope(Dispatchers.IO).launch {
                val file = File(context1.getExternalFilesDir(null), "rec${stopCounter}.txt")
                val bufferedStream = BufferedOutputStream(FileOutputStream(file, false))

                for (e in w) {
                    writeCounter += 1
                    bufferedStream.write(
                        eventToString(e.first, e.second).toByteArray()
                    )
                }

                bufferedStream.flush()
                bufferedStream.close()
                w.clear()
            }
            stopCounter += 1
        }
    }

    fun registerSensors() {
        accelerometer!!.also {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_FASTEST)
        }
    }

    fun unregisterSensors() {
        sensorManager.unregisterListener(this)
    }

    override fun onSensorChanged(event: SensorEvent) {
        onSensorChangedCounter += 1
        if (t0 == 0L) {
            t0 = System.currentTimeMillis()
        }
        cntpt = onSensorChangedCounter * 1.0 / (System.currentTimeMillis() - t0)
        val sysNano = System.nanoTime()
        assert(event.sensor.type == Sensor.TYPE_ACCELEROMETER)
        if (isRec.get()) {
            w.add(Pair(event, sysNano))
        }
    }

    private fun eventToString(e: SensorEvent, ts: Long): String {
        val d = e.values
        return "date = ${SensorEventTimeConverter.convertTimestampToReadable(ts)}, " + "timestamp = ${ts}, " + "x = ${
            String.format(
                "%.20f",
                d[0]
            )
        }, " + "y = ${String.format("%.20f", d[1])}, " + "z = ${String.format("%.20f", d[2])}\n"
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        Log.e("onAccuracyChanged", "why change")
    }
}