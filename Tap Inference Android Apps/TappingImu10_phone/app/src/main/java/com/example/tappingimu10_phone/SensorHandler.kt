package com.example.tappingimu10_phone

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Handler
import android.util.Log
import java.io.BufferedOutputStream
import java.io.File
import java.io.FileOutputStream

// the same class in previous project
class SensorHandler(private val mainActivity: MainActivity, private val handler: Handler) :
    SensorEventListener {

    private val file = File(mainActivity.filesDir, "imu_${fileTimeName}.txt")
    private val bufferedStream = BufferedOutputStream(FileOutputStream(file, true))

    private var sensorManager: SensorManager =
        mainActivity.getSystemService(Context.SENSOR_SERVICE) as SensorManager

    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null

    private var t0: Long = 0L
    private var cntpt: Double = 0.0
    private var onSensorChangedCounter: Long = 0L

    init {
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)
    }

    fun start() {
        accelerometer!!.also {
//            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL, handler)
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_FASTEST, handler)
        }
        gyroscope?.also {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_FASTEST, handler)
        }
    }

    fun stop() {
        sensorManager.unregisterListener(this)
        bufferedStream.flush()
        bufferedStream.close()
    }

    fun ff() {
        bufferedStream.flush()
    }

    override fun onSensorChanged(event: SensorEvent) {
        onSensorChangedCounter += 1

        if (onSensorChangedCounter % 1000 == 0L) {
            Log.d("tttt", "This function is running on thread: ${Thread.currentThread().name}")
            cntpt = onSensorChangedCounter * 1.0 / (System.currentTimeMillis() - t0)
            Log.e("cccc", "Rate: $cntpt Hz")
            t0 = System.currentTimeMillis()
            onSensorChangedCounter = 1
            cntpt = 0.0
//            mainActivity.bufferedStream.write("${getCurrentDateTimeFormatted()}, ${System.currentTimeMillis()}, 100\n".toByteArray());
        }

        val sysNano = System.nanoTime()
        val sensorType = when (event.sensor.type) {
            Sensor.TYPE_ACCELEROMETER -> "Acc"
            Sensor.TYPE_GYROSCOPE -> "Gyro"
            else -> "Unknown"
        }

        bufferedStream.write(eventToString(sensorType, event, sysNano).toByteArray())
    }

    private fun eventToString(tp: String, e: SensorEvent, ts: Long): String {
        val d = e.values
        return "$tp " +
                "date = ${getCurrentDateTimeFormatted()}, " +
                "timestamp = ${ts}, " +
                "x = ${String.format("%.20f", d[0])}, " +
                "y = ${String.format("%.20f", d[1])}, " +
                "z = ${String.format("%.20f", d[2])}\n"
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        Log.e("SensorAccuracyChanged", "Sensor: ${sensor?.name}, Accuracy: $accuracy")
    }
}