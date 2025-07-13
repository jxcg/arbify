import React from 'react';
import { motion } from 'framer-motion';

function ProfitSummary({ bets }) {
    const totalProfit = bets.reduce((sum, bet) => sum + bet.profit_loss, 0);

    const cardVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
    };

    return (
        <motion.div
            className="bg-white p-6 rounded-2xl shadow-md mt-6"
            initial="hidden"
            animate="visible"
            variants={cardVariants}
        >
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Overall Profit Summary</h2>
            <p className="text-gray-700 text-lg">
                Total Profit/Loss: 
                <span className={`font-bold ${totalProfit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {totalProfit.toFixed(2)}
                </span>
            </p>
        </motion.div>
    );
}

export default ProfitSummary;