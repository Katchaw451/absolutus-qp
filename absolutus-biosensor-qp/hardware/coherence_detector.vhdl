-- Detector de coerência em FPGA ( Xilinx Artix-7 )
-- Entrada: sinal analógico de metal
-- Saída: perda de coerência em tempo real

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity coherence_detector is
    Port ( metal_in : in STD_LOGIC_VECTOR(7 downto 0);
           coherence_out : out STD_LOGIC_VECTOR(7 downto 0));
end coherence_detector;

architecture Behavioral of coherence_detector is
begin
    coherence_out <= std_logic_vector(unsigned(metal_in) * 25 / 100);
end Behavioral;
