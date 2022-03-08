package application;

import com.kuka.roboticsAPI.executionModel.ExecutionState;
import com.kuka.roboticsAPI.executionModel.IExecutionContainer;
import com.kuka.roboticsAPI.motionModel.IMotion;
import com.kuka.roboticsAPI.motionModel.IMotionContainer;
import com.kuka.roboticsAPI.motionModel.IMotionContainerListener;

public class KukaIMotionContainerListener implements IMotionContainerListener {

	public boolean ACK = false;
	
	public KukaIMotionContainerListener() {
		// TODO Auto-generated constructor stub
	}

	@Override
	public void onStateChanged(IExecutionContainer container,
			ExecutionState state) {
		// TODO Auto-generated method stub

	}

	@Override
	public void containerFinished(IMotionContainer container) {
		// TODO Auto-generated method stub

	}

	@Override
	public void motionFinished(IMotion motion) {
		// TODO Auto-generated method stub
		ACK = true;
		//getLogger().info("begin askForOperator function");
	}

	@Override
	public void motionStarted(IMotion motion) {
		// TODO Auto-generated method stub
		ACK = false;
	}
	
	public boolean getACK(){
		return ACK;
	}
}

