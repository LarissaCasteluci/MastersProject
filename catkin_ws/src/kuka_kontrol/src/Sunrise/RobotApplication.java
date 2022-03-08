package application;


import java.util.List;
import java.util.concurrent.TimeUnit;

import javax.inject.Inject;
import com.kuka.roboticsAPI.applicationModel.RoboticsAPIApplication;
import static com.kuka.roboticsAPI.motionModel.BasicMotions.*;

import com.kuka.roboticsAPI.conditionModel.ICallbackAction;
import com.kuka.roboticsAPI.conditionModel.ICondition;
import com.kuka.roboticsAPI.conditionModel.JointTorqueCondition;
import com.kuka.roboticsAPI.deviceModel.Device;
import com.kuka.roboticsAPI.deviceModel.JointEnum;
import com.kuka.roboticsAPI.deviceModel.LBR;
import com.kuka.roboticsAPI.executionModel.IFiredTriggerInfo;
import com.kuka.roboticsAPI.geometricModel.CartDOF;
import com.kuka.roboticsAPI.geometricModel.Tool;
import com.kuka.roboticsAPI.motionModel.ErrorHandlingAction;
import com.kuka.roboticsAPI.motionModel.IErrorHandler;
import com.kuka.roboticsAPI.motionModel.IMotionContainer;
import com.kuka.roboticsAPI.motionModel.IMotionContainerListener;
import com.kuka.roboticsAPI.motionModel.MotionBatch;
import com.kuka.roboticsAPI.motionModel.controlModeModel.CartesianImpedanceControlMode;


/**
 * Implementation of a robot application.
 * <p>
 * The application provides a {@link RoboticsAPITask#initialize()} and a 
 * {@link RoboticsAPITask#run()} method, which will be called successively in 
 * the application lifecycle. The application will terminate automatically after 
 * the {@link RoboticsAPITask#run()} method has finished or after stopping the 
 * task. The {@link RoboticsAPITask#dispose()} method will be called, even if an 
 * exception is thrown during initialization or run. 
 * <p>
 * <b>It is imperative to call <code>super.dispose()</code> when overriding the 
 * {@link RoboticsAPITask#dispose()} method.</b> 
 * 
 * @see UseRoboticsAPIContext
 * @see #initialize()
 * @see #run()
 * @see #dispose()
 */
public class RobotApplication extends RoboticsAPIApplication {
	@Inject
	public LBR lbr;  
	public Tool tool;
	
	public double JointAcceleration;
	public double JointVelocity;
	public double JointJerk;
    
	public boolean isCollision = false;
	public boolean kukaACK = false;
	
	private IErrorHandler errorHandler;
    private IMotionContainer _currentMotion;
    
	@Override
	public void initialize() {
		// initialize your application here
		getController("KUKA_Sunrise_Cabinet_1");
		lbr = getContext().getDeviceFromType(LBR.class);
		tool = getApplicationData().createFromTemplate("tool1");
		tool.attachTo(lbr.getFlange());
		
		JointAcceleration  = 1.0;
		JointVelocity = 1.0;
		JointJerk = 1.0;
		
		errorHandler = new IErrorHandler() {
			@Override
			public ErrorHandlingAction handleError(Device device,
					                               IMotionContainer failedContainer,
					                               List<IMotionContainer> canceledContainers) {

                getLogger()
                .warn("Excecution of the following motion failed: "
                      + failedContainer.getCommand().toString());
                
                getLogger()
                .info("The following motions will not be executed:");
                
                for (int i = 0; i < canceledContainers.size(); i++) {
                    getLogger()
                        .info(canceledContainers
                        .get(i)
                        .getCommand()
                        .toString());
                }
                return ErrorHandlingAction.Ignore;
			}
        }; // IErrorHandler()
        
		getApplicationControl()
		.registerMoveAsyncErrorHandler(errorHandler);
		
	}

    public ICondition defineSensitivity() {
		//double sensCLS = getApplicationData().getProcessData("sensCLS").getValue(); // Uncomment if you have "sensCLS" defined.
		double sensCLS = 30; // Modify the value if required.
		
		double actTJ1 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J1);
		double actTJ2 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J2);
		double actTJ3 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J3);
		double actTJ4 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J4);
		double actTJ5 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J5);
		double actTJ6 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J6);
		double actTJ7 = lbr.getExternalTorque().getSingleTorqueValue(JointEnum.J7);
		
		JointTorqueCondition jt1 = new JointTorqueCondition(JointEnum.J1, -sensCLS+actTJ1, sensCLS+actTJ1);
		JointTorqueCondition jt2 = new JointTorqueCondition(JointEnum.J2, -sensCLS+actTJ2, sensCLS+actTJ2);
		JointTorqueCondition jt3 = new JointTorqueCondition(JointEnum.J3, -sensCLS+actTJ3, sensCLS+actTJ3);
		JointTorqueCondition jt4 = new JointTorqueCondition(JointEnum.J4, -sensCLS+actTJ4, sensCLS+actTJ4);
		JointTorqueCondition jt5 = new JointTorqueCondition(JointEnum.J5, -sensCLS+actTJ5, sensCLS+actTJ5);
		JointTorqueCondition jt6 = new JointTorqueCondition(JointEnum.J6, -sensCLS+actTJ6, sensCLS+actTJ6);
		JointTorqueCondition jt7 = new JointTorqueCondition(JointEnum.J7, -sensCLS+actTJ7, sensCLS+actTJ7);

		ICondition forceCon = jt1.or(jt2, jt3, jt4, jt5, jt6, jt7);
		return forceCon;
	} // public ICondition defineSensitivity
    
	public void behaviourAfterCollision() { 
		isCollision = true;
		IMotionContainer handle;
		
		CartesianImpedanceControlMode CollisionSoft = new CartesianImpedanceControlMode();
		CollisionSoft.parametrize(CartDOF.ALL).setDamping(.7);
		CollisionSoft.parametrize(CartDOF.ROT).setStiffness(100);
		CollisionSoft.parametrize(CartDOF.TRANSL).setStiffness(600);
				
		handle = tool.moveAsync(positionHold(CollisionSoft,
		                                     -1,
		                                     TimeUnit.SECONDS));

		handle.cancel();
	} // public void behaviourAfterCollision
	
    public void MoveSafe(MotionBatch MB) { 
		ICondition forceCon = defineSensitivity();
		
		ICallbackAction ica = new ICallbackAction() {
			@Override
			public void onTriggerFired(IFiredTriggerInfo triggerInformation) {
				triggerInformation.getMotionContainer().cancel();
				behaviourAfterCollision();
			}
		}; // ICallbackAction

			MB.setJointAccelerationRel(JointAcceleration)
			.setJointVelocityRel(JointVelocity)
			.triggerWhen(forceCon, ica);

		if(lbr.isReadyToMove()) {
			IMotionContainerListener myMotionContainerListener = new KukaIMotionContainerListener(kukaACK);
			IMotionContainer imc = this._currentMotion=tool.moveAsync(MB, myMotionContainerListener);
			this._currentMotion=tool.moveAsync(MB);
		}
	} // public void MoveSafe
    
	
	@Override
	public void run() {
		// your application execution starts here
		lbr.move(ptpHome());
	}
}