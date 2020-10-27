package buggy

import chisel3._
import chisel3.util._
import chisel3.formal._
import chisel3.stage.{ChiselGeneratorAnnotation, ChiselStage}


object MyUtils {
  def risingedge(x: Bool) = x && !RegNext(x)
  def fallingedge(x: Bool) = !x && RegNext(x)
}

class RisingBug extends RawModule {
  /* Input/ouput values */
  val clock = IO(Input(Clock()))
  val resetn = IO(Input(Bool()))

  val pulse = IO(Input(Bool()))

  val rise_pulse = IO(Output(Bool()))
  val fall_pulse = IO(Output(Bool()))

  withClockAndReset(clock, ~resetn) {
    rise_pulse := MyUtils.risingedge(pulse)
    fall_pulse := MyUtils.fallingedge(pulse)
  }
}


object RisingBugDriver extends App {
  (new ChiselStage).execute(args,
    Seq(ChiselGeneratorAnnotation(() => new RisingBug())))
}
