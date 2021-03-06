
/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */
#pragma once

#include <eosio/chain/chain_config.hpp>
#include <eosio/chain/types.hpp>

#include <fc/crypto/sha256.hpp>

#include <string>
#include <vector>

namespace eosio { namespace chain {

struct genesis_state {
   genesis_state();

   static const string eosio_root_key;

   chain_config   initial_configuration = {
      config::default_max_block_net_usage,
      config::default_target_block_net_usage_pct,
      config::default_max_transaction_net_usage,
      config::default_base_per_transaction_net_usage,
      config::default_net_usage_leeway,
      config::default_context_free_discount_net_usage_num,
      config::default_context_free_discount_net_usage_den,

      config::default_max_block_cpu_usage,
      config::default_target_block_cpu_usage_pct,
      config::default_max_transaction_cpu_usage,
      config::default_min_transaction_cpu_usage,

      config::default_max_trx_lifetime,
      config::default_deferred_trx_expiration_window,
      config::default_max_trx_delay,
      config::default_max_inline_action_size,
      config::default_max_inline_action_depth,
      config::default_max_auth_depth,
   };

   time_point                               initial_timestamp;
   public_key_type                          initial_key;

   /**
    * Get the chain_id corresponding to this genesis state.
    *
    * This is the SHA256 serialization of the genesis_state.
    */
   chain_id_type compute_chain_id() const;
};

} } // namespace eosio::chain


FC_REFLECT(eosio::chain::genesis_state,
           (initial_timestamp)(initial_key)(initial_configuration))
