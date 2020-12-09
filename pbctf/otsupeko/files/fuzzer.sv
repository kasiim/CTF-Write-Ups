`timescale 10ns/10ns


// Lets define our fuzzer module
module fuzzer ();
    // define same testbench signals as in original modified tb
	reg clk;
	reg n_rst;
	reg en;
	reg[6:0] next_byte;
	reg[7:0] flag_byte;
	reg win;
	// state variable to be assigned to state from challenge.v (which i added)
	reg[7:0] state;
    
	localparam CLK_PERIOD = 10ns;

    // Declare variable length arrays, which we will hold our split flags and completed flags
    // foundFlags will consist of flag splitting into different strings, will be shown later
    string foundFlags [];
    string completedFlags [];
    // counter for completed flags
    integer numOfCompletedFlags = 0;
    // Because of dummy, dummy will be used to detect if all possible splits are completed
    integer numOfFlagsFound = 1; 

    // Start off with our known prefix
	string flag = "pbctf{M4yb3_I_5h0u1d_1mp13m3nt_0n_as1c_";
	// Mark down possible characters that can be used in splits
    string splits = "";
	
    // Init challenge module
	challenge CHAL (.clk(clk), .n_rst(n_rst), .en(en), .next_byte(next_byte), .win(win), .state(state));

    // Make clock signal tick
	always begin
		clk = 1'b0;
		#(CLK_PERIOD / 2.0);
		clk = 1'b1;
		#(CLK_PERIOD / 2.0);
	end

    // Additional counters and variables
    integer asciiCharacter;
    integer flagCounter = 0;
    integer knownFlag;
    integer lastState;
    integer suitableLetter = 0;
    
    integer flagLen;
    integer splitsFound = 0;

    // While loop control bit
    bit flagsLeftToInvestigate = 1;

	initial begin
        // Make array with size of 1, populate with dummy flag
        foundFlags = new[1];
        foundFlags[0] = "Dummy";
        completedFlags = new[1];
        
        // Initialize circuit
		en = 1'b0;
		next_byte = 7'b0000000;
		n_rst = 1'b0;
		@(negedge clk);
		@(posedge clk);
		n_rst = 1'b1;
		@(negedge clk);
		@(posedge clk);

        // Fuzz untill flag = "Dummy"
        while (flagsLeftToInvestigate) begin
            // Search for max 70 chars of flag length, start from already known characters
            // Known characters are prefix + found characters
            for (flagLen = flag.len(); flagLen < 70; flagLen = flagLen + 1) begin
                splitsFound = 0;
                splits = "";
                
                // Fuzz for ascii charaters to see which trigger state change
                for (asciiCharacter = 32; asciiCharacter < 126; asciiCharacter = asciiCharacter + 1) begin
                    suitableLetter = 0;
                    
                    // This sets FSM to known state to search for possible letter
                    // So everytime we reset our FSM, we need to bring it to 
                    // wanted state, so we can check if any of the characters influence
                    // state
                    for (knownFlag = 0; knownFlag < flag.len(); knownFlag = knownFlag + 1) begin
                        @(negedge clk);
                        flag_byte = flag[knownFlag];
                        next_byte = flag_byte[6:0];
                        en = 1'b1;
                    end
                    
                    // Try new letter
                    @(negedge clk);
                    flag_byte = asciiCharacter;
                    next_byte = flag_byte[6:0];
                    en = 1'b1;
                    @(negedge clk);
                    @(posedge clk);
                    @(negedge clk);
                    
                    // If new state has stabilized check if it has changed
                    if (lastState != state && suitableLetter == 0) begin
                        suitableLetter = asciiCharacter;
                        
                        // Checked split paths before, and there are no consequtive 
                        // letters which make state changes
                        // otherwise would need to remember normal state of FSM
                        // this occurs, because lastState will be set to new state
                        // and then back to default one
                        if (suitableLetter != " " && 
                            suitableLetter != (splits[splitsFound - 1] + 1)) begin 
                            // Mark down possible splits in paths
                            splits = {splits, suitableLetter};
                            splitsFound = splitsFound + 1;
                        end
                    end
                    
                    // Update state
                    lastState = state;
                    
                    // add some delay and reset CHAL module, to inital state for fuzzing
                    @(negedge clk);
                    @(posedge clk);
                    @(negedge clk);
                    @(posedge clk);
                    @(negedge clk);
                    n_rst = 1'b0;
                    @(negedge clk);
                    @(posedge clk);
                    n_rst = 1'b1;
                    @(negedge clk);
                    @(posedge clk);
               end
               $display("Splits found: %0d", splitsFound);
               $display(splits);
               
               // If flag splits into two, push them to "stack"
               // After one path is completed, pop next one and solve it till the end
               if (splitsFound > 1) begin
                   numOfFlagsFound = numOfFlagsFound + splits.len() - 1;
                   foundFlags = new[numOfFlagsFound] (foundFlags);
                   for (flagCounter = 1; flagCounter < splits.len(); flagCounter = flagCounter + 1) begin
                        foundFlags[(numOfFlagsFound) - flagCounter] = {flag, splits[flagCounter]};
                   end
                
               end
               // If no splits are found that means, FSM is stopped and win bit is high
               if (splitsFound == 0) begin
                    // Append completed flag also break out of the 70 letter loop, it is
                    // just an magic number from development
                    numOfCompletedFlags = numOfCompletedFlags + 1;
                    completedFlags = new[numOfCompletedFlags] (completedFlags);
                    completedFlags[numOfCompletedFlags - 1] = flag;
                    $display(flag);
                    break;
                end
            //Advance to first possible split
            flag = {flag, splits[0]};
           
            end
            // Advance onto next split from found flags
            flag = foundFlags[numOfFlagsFound - 1];
            numOfFlagsFound = numOfFlagsFound - 1;
            foundFlags = new[numOfFlagsFound] (foundFlags);
            // Finish searching for additional flags, cause we are done
            if (flag == "Dummy") begin
                flagsLeftToInvestigate = 0;
            end
        end
		@(negedge clk);
		en = 0;
        for (flagCounter = 0; flagCounter < completedFlags.size; flagCounter = flagCounter + 1) begin
            if (completedFlags[flagCounter].len() != 49) begin
                $display("False!!!");
            end else begin
                $display("Correct!");
                $display(completedFlags[flagCounter]);
            end
		end
		$finish;
	end
endmodule